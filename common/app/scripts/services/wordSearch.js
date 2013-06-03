'use strict';

/* Services */


angular.module('pali.wordSearch', ['pali.ngBits']).
  factory('wordSearch', ['ngBits', function(ngBits) {
    /**
     * Succinct Data Structures for Trie
     * @see http://stevehanov.ca/blog/index.php?id=120
     */

    var MAX_NUMBER_OF_MATCHED_WORDS = 30;
    var MAX_NUMBER_OF_POSSIBLE_WORDS = 15;

    function traverseSubTrie(node, prefix, limit) {
      var words = []
      var level = [node];
      var prefixLevel = [prefix];
      while( level.length > 0 ) {
        var node2 = level.shift();
        var prefix2 = prefixLevel.shift();

        // if the 'prefix' variable is a legal pali word.
        if ( node2.final ) {
          words.push(prefix2);
          if ( words.length > limit ) return words;
        }

        for( var i = 0; i < node2.getChildCount(); i++ ) {
          var child = node2.getChild( i );
          level.push( child );
          prefixLevel.push(prefix2 + child.letter);
        }
      }

      return words;
    }

    function autoSuggestedWords(paliWord) {
      if ( paliWord.length === 0 ) return [];

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
        if ( j === node.getChildCount() ) return [];

        node = child;
      }

      // The node corresponding to the last letter of paliWord is found.
      // Use this node as root. traversing the trie in level order.
      return traverseSubTrie(node, paliWord, MAX_NUMBER_OF_MATCHED_WORDS);
    }

    function possibleWords(paliWord) {
      var node = ngBits.trie.getRoot();
      var matchedPrefix = '';

      // find the node corresponding to the last letter of prefix-matched string
      for (var i=0; i < paliWord.length; i++ ) {
        var child;
        var j = 0;
        for ( ; j < node.getChildCount(); j++ ) {
          child = node.getChild( j );
          if ( child.letter === paliWord[i] ) break;
        }

        // not found, this is the node we want
        if ( j === node.getChildCount() ) break;

        node = child;
        matchedPrefix += child.letter;
      }

      // The node corresponding to the last letter of prefix-matched string
      // Use this node as root. traversing the trie in level order.
      return [ matchedPrefix,
        traverseSubTrie(node, matchedPrefix, MAX_NUMBER_OF_POSSIBLE_WORDS)];
    }

    function getWordsStartsWithLetter(firstLetter) {
      // find node corresponding to firstLetter.
      var root = ngBits.trie.getRoot();

      var node;
      var i = 0;
      for ( ; i < root.getChildCount(); i++ ) {
        node = root.getChild( i );
        if ( node.letter === firstLetter ) break;
      }

      // not found, return empty array.
      if ( i === root.getChildCount() ) return [];

      // The node corresponding to the firstLetter is found.
      // Use this node as root. traversing the trie in level order.
      return traverseSubTrie(node, firstLetter, 1000000);
    }

    function isValidPaliWord(paliWord) {
      return ngBits.trie.lookup(paliWord);
    }

    return { isValidPaliWord: isValidPaliWord,
             autoSuggestedWords: autoSuggestedWords,
             possibleWords: possibleWords,
             getWordsStartsWithLetter: getWordsStartsWithLetter };
  }]);
