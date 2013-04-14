'use strict';

/* Services */


angular.module('pali.services', ['pali.service-dic', 'pali.dicPrefix']).
  factory('paliJson', ['$q', '$cacheFactory', 'paliIndexes', 'xhrCors', function($q, $cacheFactory, paliIndexes, xhrCors) {
    var cache = $cacheFactory('paliJson');

    function get(word) {
      var url = paliIndexes.getJsonUrl(word);

      var jsonData = cache.get(url);
      if (jsonData) {
        // cache hit: json data in cache
        var deferred = $q.defer();
        deferred.resolve(jsonData);
        return deferred.promise;
      } else {
        return xhrCors.get(url).then( function(jsonData) {
          cache.put(url, jsonData);
          return jsonData;
        }, function(reason) {
          return reason;
        });
      }
    }

    var serviceInstance = { get: get };
    return serviceInstance;
  }]).

  factory('xhrCors', ['$q', '$rootScope', function($q, $rootScope) {

    function get(url) {
      var deferred = $q.defer();

      // for IE8 CORS (angularjs $http does not support IE8 CORS)
      var xmlhttp = new window.XMLHttpRequest();

      function xdrerr() {
        deferred.reject('IE XDomainRequest failed!');
        $rootScope.$apply();
      }

      // @see http://blogs.msdn.com/b/ie/archive/2012/02/09/cors-for-xhr-in-ie10.aspx
      // @see http://bionicspirit.com/blog/2011/03/24/cross-domain-requests.html
      // @see http://msdn.microsoft.com/en-us/library/ie/cc288060(v=vs.85).aspx
      if ("withCredentials" in xmlhttp) {
        // standard compliant browsers
        xmlhttp.onreadystatechange = function() {
          if (xmlhttp.readyState == 4) {
            if (xmlhttp.status == 200 || xmlhttp.status == 304) {
              deferred.resolve( eval('(' + xmlhttp.responseText + ')') );
            } else {
              deferred.reject(xmlhttp.status);
            }
            $rootScope.$apply();
          }
        }

        xmlhttp.open("GET", url, true);
        xmlhttp.send();
      } else {
        // IE8
        var xdr = new XDomainRequest();
        xdr.onerror = xdrerr;
        xdr.ontimeout = xdrerr;
        xdr.onload = function() {
          deferred.resolve( eval('(' + xdr.responseText + ')') );
          $rootScope.$apply();
        };

        xdr.open("get", url);
        xdr.send();
      }

      return deferred.promise;
    }

    var serviceInstance = { get: get };
    return serviceInstance;
  }]).

  factory('paliIndexes', ['dicPrefix', function(dicPrefix) {

    var MAX_NUMBER_OF_MATCHED_WORDS = 30;
    var MAX_NUMBER_OF_POSSIBLE_WORDS = 10;

    /**
     * Fuzzy Map romanized pāli letters to English counterpart letters.
     * @const
     * @enum {string}
     * @private
     */
    var FuzzyCharMapping = {
      "a" : "a",
      "A" : "a",

      "ā" : "a",
      "Ā" : "a",

      "i" : "i",
      "I" : "i",

      "ī" : "i",
      "Ī" : "i",

      "u" : "u",
      "U" : "u",

      "ū" : "u",
      "Ū" : "u",

      "e" : "e",
      "E" : "e",

      "o" : "o",
      "O" : "o",

      "m" : "m",
      "M" : "m",

      "ṁ" : "m",
      "Ṁ" : "m",
      "ṃ" : "m",
      "Ṃ" : "m",
      "ŋ" : "m",
      "Ŋ" : "m",

      "n" : "n",
      "N" : "n",

      "ṇ" : "n",
      "Ṇ" : "n",

      "ṅ" : "n",
      "Ṅ" : "n",

      "ñ" : "n",
      "Ñ" : "n",

      "p" : "p",
      "P" : "p",

      "t" : "t",
      "T" : "t",

      "ṭ" : "t",
      "Ṭ" : "t",

      "c" : "c",
      "C" : "c",

      "k" : "k",
      "K" : "k",

      "b" : "b",
      "B" : "b",

      "d" : "d",
      "D" : "d",

      "ḍ" : "d",
      "Ḍ" : "d",

      "j" : "j",
      "J" : "j",

      "g" : "g",
      "G" : "g",

      "s" : "s",
      "S" : "s",

      "h" : "h",
      "H" : "h",

      "v" : "v",
      "V" : "v",

      "r" : "r",
      "R" : "r",

      "y" : "y",
      "Y" : "y",

      "l" : "l",
      "L" : "l",

      "ḷ" : "l",
      "Ḷ" : "l",

      "-" : "-"
    };


    /**
     * Check if the first letter of user input string is valid
     * @param {string} letter The first letter of user input string
     * @return {boolean}
     * @private
     */
    function isValidFirstLetter(letter) {
      for (var key in dicPrefix.WordLists) {
        if (dicPrefix.WordLists.hasOwnProperty(key) && key === letter) return true;
      }

      return false;
    }


    function processWord(paliWord) {
      if (angular.isUndefined(paliWord)) return;

      // Remove whitespace in the beginning and end of user input string
      var word = paliWord.replace(/(^\s+)|(\s+$)/g, "");

      if (word.length === 0) return;

      if (!isValidFirstLetter(word[0])) return;

      return word;
    }


    function isValidPaliWord(paliWord) {
      var word = processWord(paliWord);
      if (angular.isUndefined(word)) return false;

      for (var i=0; i < dicPrefix.WordLists[word[0]].length; i++) {
        if (word === dicPrefix.WordLists[word[0]][i]) return true;
      }
      return false;
    }


    /**
     * Given two words, determine whether they are "similar" enough (case insensitive)
     * @param {string} word1 The first word string
     * @param {string} word2 The second word string
     * @return {boolean} true if the two words are similar enough, false otherwise.
     * @private
     */
    function wordFuzzyMatch(word1, word2) {
      for (var i=0; i < word1.length; i++) {
        if (angular.isUndefined(word2[i]))
          return false;
        if (FuzzyCharMapping[ word1[i] ] !=
            FuzzyCharMapping[ word2[i] ]) {
          return false;
        }
      }
      return true;
    }


    /**
     * Given two words, determine whether they are the same (case insensitive)
     * @param {string} word1 The first word string
     * @param {string} word2 The second word string
     * @return {boolean} true if the two words are the same, false otherwise.
     * @private
     */
    function wordExactMatch(word1, word2) {
      for (var i=0; i < word1.length; i++) {
        if (angular.isUndefined(word2[i]))
          return false;
        if (word1[i].toLowerCase() != word2[i].toLowerCase())
          return false;
      }
      return true;
    }


    function prefixMatch(paliWord) {
      var word = processWord(paliWord);
      if (angular.isUndefined(word)) return;

      /**
       * Array which contains words that start with 'word[0]'
       * @type {Array}
       * @private
       */
      var array = dicPrefix.WordLists[word[0]];
      /**
       * FIXME: do something like: array[u_and_ū] = array[u].concat[array[ū]]
       */

      var prefixMatchedPaliWords = [];
      var prefixExactMatchedPaliWords = [];
      var prefixFuzzyMatchedPaliWords = [];

      for (var i=0; i < array.length; i++ ) {
        if (wordExactMatch(word, array[i])) {
          // exact prefix match of user input string and word string
          prefixExactMatchedPaliWords.push(array[i]);
        } else {
          // fuzzy prefix match of user input string and word string
          if (wordFuzzyMatch(word, array[i])) {
            prefixFuzzyMatchedPaliWords.push(array[i]);
          }
        }

        if (prefixExactMatchedPaliWords.length === MAX_NUMBER_OF_MATCHED_WORDS) break;
      }

      prefixMatchedPaliWords = prefixExactMatchedPaliWords.concat(prefixFuzzyMatchedPaliWords);

      if (prefixMatchedPaliWords.length === 0) return;
      if (prefixMatchedPaliWords.length > MAX_NUMBER_OF_MATCHED_WORDS)
        return prefixMatchedPaliWords.slice(0, MAX_NUMBER_OF_MATCHED_WORDS);
      return prefixMatchedPaliWords;
    }


    function prefixExactMatch(word) {
      // no need to call processWord() because this function is
      // only used by possibleWords(), and paliWord already processed.

      var array = dicPrefix.WordLists[word[0]];

      var prefixExactMatchedPaliWords = [];

      for (var i=0; i < array.length; i++ ) {
        if (wordExactMatch(word, array[i])) {
          // exact prefix match of user input string and word string
          prefixExactMatchedPaliWords.push(array[i]);
        }

        if (prefixExactMatchedPaliWords.length === MAX_NUMBER_OF_MATCHED_WORDS) break;
      }

      if (prefixExactMatchedPaliWords.length === 0) return;
      return prefixExactMatchedPaliWords;
    }


    function possibleWords(paliWord) {
      var word = processWord(paliWord);
      if (angular.isUndefined(word)) return;

      for (var i = word.length; i>0 ; i--) {
        var firstIPrefixMatchedWords = prefixExactMatch(word.slice(0, i));
        if (firstIPrefixMatchedWords) {
          // FIXME: ekaṃ should include eka in result, but now eka not included!!!
          if (firstIPrefixMatchedWords.length > MAX_NUMBER_OF_POSSIBLE_WORDS)
            return [word.slice(0, i), firstIPrefixMatchedWords.slice(0, MAX_NUMBER_OF_POSSIBLE_WORDS)];
          return [word.slice(0, i), firstIPrefixMatchedWords];
        }
      }
    }

    function exactPrefixMatchPossibleWords(paliWord) {
      var word = processWord(paliWord);
      if (angular.isUndefined(word)) return;
      return prefixExactMatch(word);
    }

    function longestPrefixMatchedWord(paliWord) {
      var word = processWord(paliWord);
      if (angular.isUndefined(word)) return;

      for (var i = word.length; i>0 ; i--) {
        if (isValidPaliWord(word.slice(0, i)))
          return word.slice(0, i);
      }
    }


    var serviceInstance = {
      prefixMatch: prefixMatch,
      possibleWords: possibleWords,
      exactPrefixMatchPossibleWords: exactPrefixMatchPossibleWords,
      longestPrefixMatchedWord: longestPrefixMatchedWord,
      isValidPaliWord: isValidPaliWord,

      getJsonUrl: function(word) {
        // need to check sanity of argument 'word' here?

        return 'http://jsons' + dicPrefix.Group[word[0]] +
               '.palidictionary.appspot.com/json/' +
               window.encodeURIComponent(word[0]).replace(/%/g, 'Z') + '/' +
               window.encodeURIComponent(word).replace(/%/g, 'Z') + '.json';
      },

      getWordsStartsWithLetter: function(letter) {
        if (!isValidFirstLetter(letter))
          return;
        else
          return dicPrefix.WordLists[letter];
      }
    };

    return serviceInstance;
  }]);
