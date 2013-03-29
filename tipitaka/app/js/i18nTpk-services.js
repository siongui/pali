'use strict';

/* Services */


angular.module('paliTipitaka.i18nTpk', ['pali.data.i18nTpk']).
  factory('i18nTpkServ', ['tvServ', 'i18nTpk', function(tvServ, i18nTpk) {
    function basename(str) { return str.split('/').reverse()[0]; }

    function recursiveBuildPath(node, pathPrefix, xmlFilename) {
      var path = pathPrefix + '/' + node['subpath'];
      if (path === '/canon/tipiṭaka (mūla)') path = '/canon';
      if (node.hasOwnProperty('action')) {
        if (basename(node['action']) === xmlFilename)
          return path;
      } else {
        for (var i=0; i<node['child'].length; i++) {
          var result = recursiveBuildPath(node['child'][i], path, xmlFilename);
          if (angular.isString(result))
            return result;
        }
      }
    }

    function xmlFilename2Path(xmlFilename) {
      var node = tvServ.tipitakaRootNode;
      var pathPrefix = tvServ.tipitakaRootNodePath;
      return recursiveBuildPath(node, pathPrefix, xmlFilename);
    }

    function getLocaleTranslations() {
      var localeTranslations = [];
      for (var locale in i18nTpk.translationInfo) {
        var localeTranslation = {};
        localeTranslation.locale = locale;
        localeTranslation.translations = [];
        for (var xmlFilename in i18nTpk.translationInfo[locale]['canon']) {
          var translation = {};
          translation.path = xmlFilename2Path(xmlFilename);
          if (i18nTpk.canonName[xmlFilename].hasOwnProperty(locale)) {
            translation.canonName = i18nTpk.canonName[xmlFilename][locale];
          } else {
            translation.canonName = i18nTpk.canonName[xmlFilename]['pali'];
          }
          translation.translatorCode = i18nTpk.translationInfo[locale]['canon'][xmlFilename];
          translation.translator =  i18nTpk.translationInfo[locale]['source'][translation.translatorCode][0];
          localeTranslation.translations.push(translation);
        }
        localeTranslations.push(localeTranslation);
      }
      return localeTranslations;
    }

    function getTranslatorCode(locale, xmlFilename, translator) {
      var translatorCodes = i18nTpk.translationInfo[locale]['canon'][xmlFilename];
      if (!angular.isArray(translatorCodes))
        throw 'In getTranslatorCode: no codes';

      for (var i=0; i<translatorCodes.length; i++) {
        if (translator === i18nTpk.translationInfo[locale]['source'][translatorCodes[i]][0])
          return translatorCodes[i];
      }

      throw 'In getTranslatorCode: cannot find translator code';
    }

    function getTranslationXmlUrl(canonPath, locale, translator) {
      var info = tvServ.getInfo('/canon/' + canonPath);
      if (!info.hasOwnProperty('action')) {
        // not leaf node => impossible => FIXME: do error handling here
        throw 'In getTranslationUrl: no action';
        return;
      }
      var xmlFilename = basename(info.action);
      var translatorCode = getTranslatorCode(locale, xmlFilename, translator);
      return '/translation/' + locale + '/'+ translatorCode + '/' + xmlFilename;
    }

    function getI18nLinks(action) {
      var xmlFilename = basename(action);
      var localeTranslations = [];
      for (var locale in i18nTpk.translationInfo) {
        var localeTranslation = {};
        localeTranslation.locale = locale;
        localeTranslation.translations = [];
        if (i18nTpk.translationInfo[locale]['canon'].hasOwnProperty(xmlFilename)) {
          var translation = {};
          translation.path = xmlFilename2Path(xmlFilename);
          translation.canonName = i18nTpk.canonName[xmlFilename]['pali'];
          translation.translatorCode = i18nTpk.translationInfo[locale]['canon'][xmlFilename];
          translation.translator =  i18nTpk.translationInfo[locale]['source'][translation.translatorCode][0];
          localeTranslation.translations.push(translation);
        }
        if (localeTranslation.translations.length > 0)
          localeTranslations.push(localeTranslation);
      }
      if (localeTranslations.length > 0)
        return localeTranslations;
    }

    function translateText(text, locale) {
      // remove leading un-needed characters
      var str = text.replace(/^[\d\s()-\.]+/, '');
      // remove trailing un-needed characters
      str = str.replace(/-\d$/, '');

      if (i18nTpk.canonTextTranslation.hasOwnProperty(locale)) {
        if (i18nTpk.canonTextTranslation[locale].hasOwnProperty(str)) {
          return i18nTpk.canonTextTranslation[locale][str];
        }
      }

      return text;
    }

    var serviceInstance = {
      translateText: translateText,
      getI18nLinks: getI18nLinks,
      getLocaleTranslations: getLocaleTranslations,
      getTranslationXmlUrl: getTranslationXmlUrl
    };
    return serviceInstance;
  }]);
