'use strict';

/* Filters */

angular.module('pali.filters', []).
  filter('zhConvert', ['zhService', function(zhService) {
    return function(dicWordExps, setting) {
      if (setting.toTraditionalCht) {
        angular.forEach(dicWordExps, function(dicWordExp) {
          dicWordExp[0] = zhService.toTrad(dicWordExp[0]);
          dicWordExp[2] = zhService.toTrad(dicWordExp[2]);
        });
      }
      return dicWordExps;
    }
  }]).

  filter('removeFuzzyMatch', [function() {
    return function(dicWordExps, word) {
      var result = [];
      angular.forEach(dicWordExps, function(dicWordExp) {
        if (dicWordExp[1].toLowerCase() === word)
          result.push(dicWordExp);
      });
      return result;
    }
  }]).

  filter('dicLangSelect', ['palidic', function(palidic) {
    return function(dicWordExps, setting) {
      var result = [];
      angular.forEach(dicWordExps, function(dicWordExp) {
        var lang = palidic.lang(dicWordExp);
        if (lang === 'zh' && !setting.p2zh) return;
        if (lang === 'ja' && !setting.p2ja) return;
        if (lang === 'en' && !setting.p2en) return;
        result.push(dicWordExp);
      });
      return result;
    }
  }]).

  filter('dicOrder', ['palidic', '$rootScope', '$filter', function(palidic, $rootScope, $filter) {
    return function(dicWordExps, setting) {
      // function for orderBy
      function dicOrder(dicWordExp) {
        var mapping = {};
        if (setting.dicLangOrder === 'hdr') {
          var count = 0;
          angular.forEach($rootScope.i18nLangQs, function(langQ) {
            // en_US <-- langQ[0]
            // en    <-- langQ[0].slice(0,2).toLowerCase()
            var shortLang = langQ[0].slice(0,2).toLowerCase();
            if (!mapping.hasOwnProperty(shortLang)) {
              mapping[shortLang] = count;
              count ++;
            }
          });
          if (!mapping.hasOwnProperty('en')) {
            mapping['en'] = count;
            count ++;
          }
          if (!mapping.hasOwnProperty('ja')) {
            mapping['ja'] = count;
            count ++;
          }
          if (!mapping.hasOwnProperty('zh')) {
            mapping['zh'] = count;
            count ++;
          }
          mapping['unknown'] = count;
        } else {
          var langs = setting.dicLangOrder.split('2');
          for (var i=0; i<langs.length; i++) {mapping[langs[i]] = i;}
          mapping['unknown'] = 100;
        }
        return mapping[palidic.lang(dicWordExp)];
      }

      return $filter('orderBy')(dicWordExps, dicOrder);
    }
  }]).

  filter('moveToTop', [function() {
    return function(dicWordExps, opt_dicWordExp) {
      if (angular.isUndefined(opt_dicWordExp)) {
        return dicWordExps;
      } else {
        var result = [];
        angular.forEach(dicWordExps, function(dicWordExp) {
          if (dicWordExp[0] === opt_dicWordExp[0])
            result.unshift(dicWordExp);
          else
            result.push(dicWordExp);
        });
        return result;
      }
    }
  }]);
