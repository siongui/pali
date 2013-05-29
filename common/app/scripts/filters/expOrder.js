'use strict';

/* Filters */

angular.module('pali.expOrder', []).
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
