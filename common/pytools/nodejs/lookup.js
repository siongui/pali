/**
 * Decode json data from file, and use it to check if a word exists in the
 * dictionary.
 */
var json = require(require('path').resolve(__dirname,
     '../../gae/libs/json/succinct_trie.json'));
var bitsjs = require(require('path').resolve(__dirname, 'Bits.js'));
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
