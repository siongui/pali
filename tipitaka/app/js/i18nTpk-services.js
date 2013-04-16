'use strict';

/* Services */


angular.module('paliTipitaka.i18nTpk', ['pali.data.i18nTpk']).
  factory('i18nTpkServ', ['tvServ', 'i18nTpk', 'i18nTpkConvert', function(tvServ, i18nTpk, i18nTpkConvert) {
    function getAllLocalesTranslations() {
      var localeTranslations = [];
      for (var locale in i18nTpk.translationInfo) {
        var localeTranslation = { locale: locale };
        localeTranslation.translations = [];
        for (var xmlFilename in i18nTpk.translationInfo[locale]['canon']) {
          var translation = { xmlFilename: xmlFilename };
          translation.translatorCodes = [];
          for (var i=0; i<i18nTpk.translationInfo[locale]['canon'][xmlFilename].length; i++) {
            translation.translatorCodes.push(i18nTpk.translationInfo[locale]['canon'][xmlFilename][i]);
          }
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
      var xmlFilename = i18nTpkConvert.basename(info.action);
      var translatorCode = getTranslatorCode(locale, xmlFilename, translator);
      return '/translation/' + locale + '/'+ translatorCode + '/' + xmlFilename;
    }

    function getI18nLinks(action) {
      var xmlFilename = i18nTpkConvert.basename(action);
      var localeTranslations = [];
      for (var locale in i18nTpk.translationInfo) {
        var localeTranslation = { locale: locale };
        localeTranslation.translations = [];
        if (i18nTpk.translationInfo[locale]['canon'].hasOwnProperty(xmlFilename)) {
          var translation = { xmlFilename: xmlFilename };
          translation.translatorCodes = [];
          for (var i=0; i<i18nTpk.translationInfo[locale]['canon'][xmlFilename].length; i++) {
            translation.translatorCodes.push(i18nTpk.translationInfo[locale]['canon'][xmlFilename][i]);
          }
          localeTranslation.translations.push(translation);
        }
        if (localeTranslation.translations.length > 0)
          localeTranslations.push(localeTranslation);
      }
      if (localeTranslations.length > 0)
        return localeTranslations;
    }

    var serviceInstance = {
      getI18nLinks: getI18nLinks,
      getAllLocalesTranslations: getAllLocalesTranslations,
      getTranslationXmlUrl: getTranslationXmlUrl
    };
    return serviceInstance;
  }]).

  factory('i18nTpkConvert', ['$location', 'tvServ', 'i18nTpk', function($location, tvServ, i18nTpk) {
    function basename(str) { return str.split('/').reverse()[0]; }

    function endswith(str, suffix) {
      return str.indexOf(suffix, str.length - suffix.length) != -1;
    }

    function nodeTextStrip(text) {
      // remove leading and trailing un-needed characters
      return text.replace(/^[\d\s()-\.]+/, '').replace(/-\d$/, '');
    }

    function nodeTextStrip2(text) {
      var str = nodeTextStrip(text); 
      if (endswith(str, 'pāḷi'))
        return str.slice(0, -4);
      if (endswith(str, 'nikāya'))
        return str.slice(0, -6);
      if (endswith(str, 'piṭaka'))
        return str.slice(0, -6);
      return str;
    }

    function translateNodeText(text, locale) {
      var str = nodeTextStrip(text);

      if (i18nTpk.canonTextTranslation.hasOwnProperty(locale)) {
        if (i18nTpk.canonTextTranslation[locale].hasOwnProperty(str)) {
          return i18nTpk.canonTextTranslation[locale][str];
        }
      }

      return text;
    }

    function translateNodeText2(text, locale) {
      var str = nodeTextStrip(text);
      var trStr = translateNodeText(text, locale);
      if (trStr === text)
        return text;
      else
        return text.replace(str, trStr);
    }

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

    function getTranslator(locale, translatorCode) {
      return i18nTpk.translationInfo[locale]['source'][translatorCode][0];
    }

    function recursiveGetCanonName(node, names, xmlFilename) {
      if (node.hasOwnProperty('action')) {
        if (basename(node['action']) === xmlFilename) {
          names.push(nodeTextStrip2(node['text']));
          return names;
        }
      } else {
        for (var i=0; i<node['child'].length; i++) {
          var result = recursiveGetCanonName(node['child'][i], names, xmlFilename);
          if (angular.isArray(result)) {
            names.push(nodeTextStrip2(node['text']));
            return result;
          }
        }
      }
    }

    function xmlFilename2CanonName(xmlFilename) {
      return recursiveGetCanonName(tvServ.tipitakaRootNode, [], xmlFilename);
    }

    function recursiveGetTranslatedCanonName(node, names, xmlFilename, locale) {
      var trName = translateNodeText(node['text'], locale);
      if (trName === node['text']) trName = '';

      if (node.hasOwnProperty('action')) {
        if (basename(node['action']) === xmlFilename) {
          names.push(trName);
          return names;
        }
      } else {
        for (var i=0; i<node['child'].length; i++) {
          var result = recursiveGetTranslatedCanonName(node['child'][i], names, xmlFilename, locale);
          if (angular.isArray(result)) {
            names.push(trName);
            return result;
          }
        }
      }
    }

    function xmlFilename2TranslatedCanonName(xmlFilename, locale) {
      return recursiveGetTranslatedCanonName(tvServ.tipitakaRootNode, [], xmlFilename, locale);
    }

    function redirectAccordingToUrlLocale(path) {
      if ($location.path().indexOf('/en_US/') === 0) {
        $location.path('/en_US' + path);
      } else if ($location.path().indexOf('/zh_TW/') === 0) {
        $location.path('/zh_TW' + path);
      } else if ($location.path().indexOf('/zh_CN/') === 0) {
        $location.path('/zh_CN' + path);
      } else {
        $location.path(path);
      }
    }

    var serviceInstance = {
      translateNodeText: translateNodeText,
      translateNodeText2: translateNodeText2,
      getTranslator: getTranslator,
      xmlFilename2CanonName: xmlFilename2CanonName,
      xmlFilename2TranslatedCanonName: xmlFilename2TranslatedCanonName,
      xmlFilename2Path: xmlFilename2Path,
      redirectAccordingToUrlLocale: redirectAccordingToUrlLocale,
      basename: basename
    };
    return serviceInstance;
  }]);
