'use strict';

/* Services */


angular.module('pali.wordSearch', ['pali.ngBits']).
  factory('wordSearch', ['ngBits', function(ngBits) {
    /**
     * Succinct Data Structures for Trie
     * @see http://stevehanov.ca/blog/index.php?id=120
     */

    var MAX_NUMBER_OF_MATCHED_WORDS = 30;

    function autoSuggestedWords(paliWord) {
      if ( paliWord.length === 0 ) return [];

      var exactMatchedArray = [];
      var node = ngBits.trie.getRoot();

      // find the node corresponding to the last letter of paliWord
      for (var i=0; i < paliWord.length; i++ ) {
        var child;
        var j = 0;
        for ( ; j < node.getChildCount(); j++ ) {
          child = node.getChild( j );
          if ( child.letter === paliWord[i] ) break;
        }

        // not found, return empty array.
        if ( j === node.getChildCount() ) return exactMatchedArray;

        node = child;
      }

      // The node corresponding to the last letter of paliWord is found.
      // Use this node as root. traversing the trie in level order.
      var level = [node];
      var prefixLevel = [paliWord];
      while( level.length > 0 ) {
        var node2 = level.shift();
        var prefix = prefixLevel.shift();

        // if the 'prefix' variable is a legal pali word.
        if ( node2.final ) {
          exactMatchedArray.push(prefix);
          if ( exactMatchedArray.length > MAX_NUMBER_OF_MATCHED_WORDS ) {
            return exactMatchedArray;
          }
        }

        for( var i = 0; i < node2.getChildCount(); i++ ) {
          var child = node2.getChild( i );
          level.push( child );
          prefixLevel.push(prefix + child.letter);
        }
      }

      return exactMatchedArray;
    }

    function isValidPaliWord(paliWord) {
      return ngBits.trie.lookup(paliWord);
    }

    return { isValidPaliWord: isValidPaliWord,
             autoSuggestedWords: autoSuggestedWords };
  }]);
