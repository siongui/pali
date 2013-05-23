#!/usr/bin/env python
# -*- coding:utf-8 -*-

# http://ejohn.org/blog/javascript-trie-performance-analysis/
# http://stevehanov.ca/blog/index.php?id=120
# http://stevehanov.ca/blog/index.php?id=115

import os
import json

def buildTrie(wordsDir):
  trie = {}

  for dirpath, dirnames, filenames in os.walk(dictWordsJsonDir):
    for filename in filenames:
      # loop through words (filename is actually a word)
      word = filename.decode('utf-8')
      # position starts from the head of trie
      pos = trie

      for index, letter in enumerate(word):
        # loop through the letters in the word

        if letter not in pos:
          pos[letter] = {}
          pos = pos[letter]
          if index == len(word) - 1:
            # mark the end of the word
            pos['$'] = 1
        else:
          pos = pos[letter]
          if index == len(word) - 1:
            # mark the end of the word
            pos['$'] = 1

  return trie


if __name__ == '__main__':
  dictWordsJsonDir = os.path.join(os.path.dirname(__file__), 'paliwords')
  jsonIndexPath = os.path.join(os.path.dirname(__file__), 'trie.json')
  trie = buildTrie(dictWordsJsonDir)
  #print(json.dumps(trie, sort_keys=True,
  #                 indent=2, separators=(',', ': ')))
  #print(trie)
  with open(jsonIndexPath, 'w') as f:
    f.write(json.dumps(trie))
