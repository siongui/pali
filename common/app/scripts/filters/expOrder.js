'use strict';

/* Filters */

angular.module('pali.expOrder', []).
  filter('dicLangSelect', [function() {
    return function(bookExps, settingBooksIndexArray) {
      var setting = settingBooksIndexArray[0];
      var booksIndex = settingBooksIndexArray[1];
      var result = [];
      angular.forEach(bookExps, function(bookExp) {
        var lang = booksIndex[bookExp[0]][0];
        if (lang === 'zh' && !setting.p2zh) return;
        if (lang === 'ja' && !setting.p2ja) return;
        if (lang === 'en' && !setting.p2en) return;
        if (lang === 'vi' && !setting.p2vi) return;
        if (lang === 'my' && !setting.p2my) return;
        result.push(bookExp);
      });
      return result;
    }
  }]).

  filter('dicOrder', ['$rootScope', '$filter', function($rootScope, $filter) {
    return function(bookExps, settingBooksIndexArray) {
      var setting = settingBooksIndexArray[0];
      var booksIndex = settingBooksIndexArray[1];
      var i18nLangQs = $rootScope.i18nLangQs;

      var mapping = {};
      if (setting.dicLangOrder === 'hdr') {
        var count = 0;
        angular.forEach(i18nLangQs, function(langQ) {
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
        if (!mapping.hasOwnProperty('vi')) {
          mapping['vi'] = count;
          count ++;
        }
        if (!mapping.hasOwnProperty('my')) {
          mapping['my'] = count;
          count ++;
        }
      } else {
        mapping['en'] = 1;
        mapping['ja'] = 2;
        mapping['zh'] = 3;
        mapping['vi'] = 4;
        mapping['my'] = 5;
        mapping[setting.dicLangOrder] = 0;
      }

      // function for orderBy
      function dicOrder(bookExp) {
        return mapping[booksIndex[bookExp[0]][0]];
      }

      return $filter('orderBy')(bookExps, dicOrder);
    }
  }]).

  filter('moveToTop', [function() {
    return function(bookExps, opt_bookExp) {
      if (angular.isUndefined(opt_bookExp)) {
        return bookExps;
      } else {
        var result = [];
        angular.forEach(bookExps, function(bookExp) {
          if (bookExp[0] === opt_bookExp[0])
            result.unshift(bookExp);
          else
            result.push(bookExp);
        });
        return result;
      }
    }
  }]);
