/**
 * Bits.js: A Succinct Trie for Javascript By Steve Hanov
 * @see http://stevehanov.ca/blog/index.php?id=120
 * @see http://www.hanovsolutions.com/trie/Bits.js
 * @see also https://github.com/jeresig/trie-js
 */
var bitsjs = require(require('path').resolve(__dirname, 'Bits.js'));

//var parsedJson = require(require('path').resolve(__dirname, '../trie.json'));

var words = require("fs").readdirSync('../testwords/');
words.sort();

// create a trie
var trie = new bitsjs.Trie();

for (var i=0; i < words.length; i++) {
  console.log(words[i]);
  // the following is not a correct insert usage
  // because Bits.js only accept a-z.
  trie.insert(words[i]);
}

console.log(trie);

// encode the trie
var trieData = trie.encode();

console.log(trieData);
