'use strict';

/* Services */


angular.module('paliTipitaka.i18nTpk', ['pali.data.i18nTpk']).
  factory('i18nTpkServ', ['tvServ', 'i18nTpk', 'i18nTpkConvert', function(tvServ, i18nTpk, i18nTpkConvert) {
    var xmlFilename2PathInfo = {};
    var trTextInfo = {};

    function basename(str) { return str.split('/').reverse()[0]; }

    function getTranslatedCanonName(text) {
      if (trTextInfo.hasOwnProperty(text))
        return trTextInfo[text];

      var trText = {};
      var locales = ['en_US', 'zh_TW', 'zh_CN'];
      for (var i=0; i < locales.length; i++) {
        trText[locales[i]] = i18nTpkConvert.translateNodeText(text, locales[i]);
        if (trText[locales[i]] === text) trText[locales[i]] = '';
      }
      trTextInfo[text] = trText;
      return trText;
    }

    function recursiveGetInfo(node, pathPrefix, canonNames, translatedCanonNames, xmlFilename) {
      if (node.hasOwnProperty('subpath'))
        var path = pathPrefix + '/' + node['subpath'];
      else
        var path = pathPrefix;

      if (node.hasOwnProperty('action')) {
        if (basename(node['action']) === xmlFilename) {
          canonNames.push(i18nTpkConvert.nodeTextStrip2(node['text']));
          translatedCanonNames.push(getTranslatedCanonName(node['text']));
          return { path: path, canonNames: canonNames, translatedCanonNames: translatedCanonNames };
        }
      } else {
        for (var i=0; i<node['child'].length; i++) {
          var result = recursiveGetInfo(node['child'][i], path, canonNames, translatedCanonNames, xmlFilename);
          if (angular.isObject(result)) {
            if (node.hasOwnProperty('text')) {
              result.canonNames.push(i18nTpkConvert.nodeTextStrip2(node['text']));
              result.translatedCanonNames.push(getTranslatedCanonName(node['text']));
            }
            return result;
          }
        }
      }
    }

    function xmlFilename2Info(xmlFilename) {
      if (xmlFilename2PathInfo.hasOwnProperty(xmlFilename))
        return xmlFilename2PathInfo[xmlFilename];

      var result = recursiveGetInfo(tvServ.allPali, '', [], [], xmlFilename);
      if (angular.isUndefined(result)) {
        throw 'cannot find ' + xmlFilename;
      } else {
        xmlFilename2PathInfo[xmlFilename] = result;
        return result;
      }
    }

    function getTranslator(locale, localeXmlTranslation) {
      return i18nTpk.translationInfo[locale]['source'][ localeXmlTranslation['source'] ][0];
    }

    function getLocaleXmlTranslations(translationLocale, xmlFilename) {
      var localeXmlTranslations = [];
      for (var i=0; i<i18nTpk.translationInfo[translationLocale]['canon'][xmlFilename].length; i++) {
        // ith translation of "translationLocale" and "xmlFilename"
        var tmp = i18nTpk.translationInfo[translationLocale]['canon'][xmlFilename][i];

        var localeXmlTranslation = {};
        localeXmlTranslation.translator = getTranslator(translationLocale, tmp);
        localeXmlTranslation.excerpt = tmp['excerpt'];

        localeXmlTranslations.push(localeXmlTranslation);
      }
      return localeXmlTranslations;
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
                              translatedCanonNames: info.translatedCanonNames,
                              canonNames: info.canonNames };
          translation.localeXmlTranslations = getLocaleXmlTranslations(locale, xmlFilename);
          localeTranslation.translations.push(translation);
        }
        if (localeTranslation.translations.length > 0)
          localeTranslations.push(localeTranslation);
      }
      return localeTranslations;
    }

    function getTranslatorCode(locale, xmlFilename, translator) {
      var localeXmlTranslations = i18nTpk.translationInfo[locale]['canon'][xmlFilename];
      if (!angular.isArray(localeXmlTranslations))
        throw 'In getTranslatorCode: no codes';

      for (var i=0; i<localeXmlTranslations.length; i++) {
        if (translator === i18nTpk.translationInfo[locale]['source'][ localeXmlTranslations[i]['source'] ][0])
          return localeXmlTranslations[i]['source'];
      }

      throw 'In getTranslatorCode: cannot find translator code';
    }

    function getTranslationXmlUrl(action, locale, translator) {
      var xmlFilename = basename(action);
      var translatorCode = getTranslatorCode(locale, xmlFilename, translator);
      return '/translation/' + locale + '/'+ translatorCode + '/' + xmlFilename;
    }

    function getXmlLocaleTranslationInfo(action, translationLocale, translator) {
      var info = { isExcerpt: undefined, translationCopyrightURL: undefined };
      var xmlFilename = basename(action);
      var localeXmlTranslations = i18nTpk.translationInfo[translationLocale]['canon'][xmlFilename];
      for (var i=0; i<localeXmlTranslations.length; i++) {
        if (translator === i18nTpk.translationInfo[translationLocale]['source'][ localeXmlTranslations[i]['source'] ][0]) {
          if (localeXmlTranslations[i]['excerpt']) info.isExcerpt = true;
          if (angular.isDefined(localeXmlTranslations[i]['copyrightURL'])) info.translationCopyrightURL = localeXmlTranslations[i]['copyrightURL'];
          break;
        }
      }
      return info;
    }

    function getI18nLinks(action) {
      var xmlFilename = basename(action);
      var localeTranslations = [];
      for (var locale in i18nTpk.translationInfo) {
        var localeTranslation = { locale: locale };
        localeTranslation.translations = [];
        if (i18nTpk.translationInfo[locale]['canon'].hasOwnProperty(xmlFilename)) {
          var translation = { xmlFilename: xmlFilename,
                              path: xmlFilename2Info(xmlFilename).path };
          translation.localeXmlTranslations = getLocaleXmlTranslations(locale, xmlFilename);
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
      getXmlLocaleTranslationInfo: getXmlLocaleTranslationInfo,
      getTranslationXmlUrl: getTranslationXmlUrl
    };
    return serviceInstance;
  }]).

  factory('i18nTpkConvert', ['$location', 'i18nTpk', function($location, i18nTpk) {
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
      if (endswith(str, 'piṭaka (aṭṭhakathā)'))
        return str.slice(0, -19);
      if (endswith(str, '-aṭṭhakathā')) {
        if (endswith(str, 'kaṇḍa-aṭṭhakathā'))
          return str.slice(0, -16);
        else
          return str.slice(0, -11);
      }
      if (endswith(str, 'nikāya (aṭṭhakathā)')) {
        if (endswith(str, ' nikāya (aṭṭhakathā)'))
          return str.slice(0, -20);
        else
          return str.slice(0, -19);
      }
      if (endswith(str, 'piṭaka (ṭīkā)'))
        return str.slice(0, -13);
      if (endswith(str, 'nikāya (ṭīkā)'))
        return str.slice(0, -13);
      if (endswith(str, '-mūlaṭīkā'))
        return str.slice(0, -9);
      if (endswith(str, '-ṭīkā'))
        return str.slice(0, -5);
      return str;
    }

    function gettextCanonName(name, locale) {
      if (i18nTpk.canonTextTranslation.hasOwnProperty(locale)) {
        if (i18nTpk.canonTextTranslation[locale].hasOwnProperty(name)) {
          return i18nTpk.canonTextTranslation[locale][name];
        }
      }
      return name;
    }

    function gettextFuzzyCanonName(name, locale) {
      var trName = gettextCanonName(name, locale);
      if (trName !== name)
        return trName;
      trName = gettextCanonName(name + 'pāḷi', locale);
      if (trName !== (name + 'pāḷi'))
        return trName;
      return name;
    }

    function translateNodeText(text, locale) {
      var str = nodeTextStrip(text);
      var trText = gettextCanonName(str, locale)
      if (trText == str) {
        if (endswith(trText, ' (aṭṭhakathā)')) {
          return gettextCanonName(text.slice(0, -13), locale) + ' ' +
                 gettextCanonName('Aṭṭhakathā', locale);
        }
        if (endswith(trText, '-aṭṭhakathā')) {
          return gettextFuzzyCanonName(text.slice(0, -11), locale) + ' ' +
                 gettextCanonName('Aṭṭhakathā', locale);
        }
        if (endswith(trText, ' (ṭīkā)')) {
          return gettextCanonName(text.slice(0, -7), locale) + ' ' +
                 gettextCanonName('Tīkā', locale);
        }
        if (endswith(trText, '-ṭīkā')) {
          return gettextFuzzyCanonName(text.slice(0, -5), locale) + ' ' +
                 gettextCanonName('Tīkā', locale);
        }
        return text;
      }
      return trText;
    }

    function translateNodeText2(text, locale) {
      var str = nodeTextStrip(text);
      var trStr = translateNodeText(text, locale);
      if (trStr === text)
        return text;
      else
        return text.replace(str, trStr);
    }

    function translateNodeText3(text, locale) {
      var trStr = translateNodeText(text, locale);
      if (trStr === text)
        return '';
      else
        return ' (' + trStr + ')';
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
      translateNodeText3: translateNodeText3,
      redirectAccordingToUrlLocale: redirectAccordingToUrlLocale
    };
    return serviceInstance;
  }]);
