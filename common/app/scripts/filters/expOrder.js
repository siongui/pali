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
