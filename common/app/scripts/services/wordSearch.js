'use strict';

/* Services */


angular.module('pali.wordSearch', ['pali.ngBits']).
  factory('wordSearch', ['ngBits', function(ngBits) {

    function isValidPaliWord(paliWord) {
      return ngBits.trie.lookup(paliWord);
    }

    return { isValidPaliWord: isValidPaliWord };
  }]);
