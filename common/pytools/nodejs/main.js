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
  trie.insert(words[i]);
}

// encode the trie
var trieData = trie.encode();

// Encode the rank directory
var directory = bitsjs.CreateRankDirectory( trieData, trie.getNodeCount() * 2 + 1);

var output;
    output = '{\n    "nodeCount": ' + trie.getNodeCount() + ",\n";
    output += '    "directory": "' + directory.getData() + '",\n';
    output += '    "trie": "' + trieData + '"\n';
    output += "}\n";

console.log(output);

/**
 * Decode the data in the output variable, and use it to check if a word exists
 * in the dictionary.
 */
var json = eval( '(' + output + ")" );
var ftrie = new bitsjs.FrozenTrie( json.trie, json.directory, json.nodeCount);

// @see http://nodejs.org/api/readline.html#readline_example_tiny_cli
var readline = require('readline'),
    rl = readline.createInterface(process.stdin, process.stdout);

rl.setPrompt('word> ');
rl.prompt();

rl.on('line', function(line) {
  console.log('looking up ' + line.trim() + ' ...' );
  console.log(ftrie.lookup(line.trim()));
  rl.prompt();
}).on('close', function() {
  console.log('\nEnd of lookup');
  process.exit(0);
});
