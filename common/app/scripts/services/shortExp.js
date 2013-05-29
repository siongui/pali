'use strict';

/* Service for short explanation of the word */


angular.module('pali.shortExp', []).
  factory('shortExp', [function() {

    function get(bookExp, booksIndex) {
      var separator = booksIndex[bookExp[0]][1];
      var breakPos = bookExp[1].indexOf(separator);
      if (breakPos == -1)
        var shortExp = bookExp[1];
      else
        var shortExp = bookExp[1].slice(0, breakPos);

      if (shortExp.length > 200)
        shortExp = shortExp.slice(0, 200) + ' ...';

      return shortExp;
    }

    return { get: get };
  }]);
