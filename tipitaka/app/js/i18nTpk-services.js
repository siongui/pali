'use strict';

/* Services */


angular.module('paliTipitaka.i18nTpk', ['pali.data.i18nTpk']).
  factory('i18nTpkServ', ['tvServ', 'i18nTpk', 'i18nTpkConvert', function(tvServ, i18nTpk, i18nTpkConvert) {
    var xmlFilename2PathInfo = {};

    function recursiveGetInfo(node, pathPrefix, canonNames, xmlFilename) {
      var path = pathPrefix + '/' + node['subpath'];
      if (path === '/canon/tipiṭaka (mūla)') path = '/canon';
      if (node.hasOwnProperty('action')) {
        if (i18nTpkConvert.basename(node['action']) === xmlFilename) {
          canonNames.push(i18nTpkConvert.nodeTextStrip2(node['text']));
          return { path: path, canonNames: canonNames };
        }
      } else {
        for (var i=0; i<node['child'].length; i++) {
          var result = recursiveGetInfo(node['child'][i], path, canonNames, xmlFilename);
          if (angular.isObject(result)) {
            result.canonNames.push(i18nTpkConvert.nodeTextStrip2(node['text']));
            return result;
          }
        }
      }
    }

    function xmlFilename2Info(xmlFilename) {
      if (xmlFilename2PathInfo.hasOwnProperty(xmlFilename))
        return xmlFilename2PathInfo[xmlFilename];

      var result = recursiveGetInfo(tvServ.tipitakaRootNode, tvServ.tipitakaRootNodePath, [], xmlFilename);
      if (angular.isUndefined(result)) {
        throw 'cannot find ' + xmlFilename;
      } else {
        xmlFilename2PathInfo[xmlFilename] = result;
        return result;
      }
    }

    function getTranslator(locale, translatorCode) {
      return i18nTpk.translationInfo[locale]['source'][translatorCode][0];
    }

    function getAllLocalesTranslations() {
      var localeTranslations = [];
      for (var locale in i18nTpk.translationInfo) {
        var localeTranslation = { locale: locale };
        localeTranslation.translations = [];
        for (var xmlFilename in i18nTpk.translationInfo[locale]['canon']) {
          var info = xmlFilename2Info(xmlFilename);
          var translation = { xmlFilename: xmlFilename,
                              path: info.path,
                              canonNames: info.canonNames };
          translation.translators = [];
          for (var i=0; i<i18nTpk.translationInfo[locale]['canon'][xmlFilename].length; i++) {
            translation.translators.push(getTranslator(locale, i18nTpk.translationInfo[locale]['canon'][xmlFilename][i]));
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
          var translation = { xmlFilename: xmlFilename,
                              path: xmlFilename2Info(xmlFilename).path };
          translation.translators = [];
          for (var i=0; i<i18nTpk.translationInfo[locale]['canon'][xmlFilename].length; i++) {
            translation.translators.push(getTranslator(locale, i18nTpk.translationInfo[locale]['canon'][xmlFilename][i]));
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
      nodeTextStrip2: nodeTextStrip2,
      translateNodeText: translateNodeText,
      translateNodeText2: translateNodeText2,
      xmlFilename2TranslatedCanonName: xmlFilename2TranslatedCanonName,
      redirectAccordingToUrlLocale: redirectAccordingToUrlLocale,
      basename: basename
    };
    return serviceInstance;
  }]);
