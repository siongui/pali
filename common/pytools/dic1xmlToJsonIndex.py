#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys
import xml.dom.minidom
import json

# @see https://developers.google.com/appengine/docs/python/runtime#Quotas_and_Limits
# maximum total number of files (app files and static files): 10,000 per directory
# @see https://developers.google.com/appengine/docs/quotas#Deployments
# An application is limited to 10,000 uploaded files per version.

fuzzyChars = {
  u"ā" : u"a",
  u"ī" : u"i",
  u"ū" : u"u",
  u"ṁ" : u"m",
  u"ṃ" : u"m",
  u"ŋ" : u"m",
  u"ṇ" : u"n",
  u"ṅ" : u"n",
  u"ñ" : u"n",
  u"ṭ" : u"t",
  u"ḍ" : u"d",
  u"ḷ" : u"l",
}

if __name__ == '__main__':
  srcXmlDir = os.path.join(os.path.dirname(__file__), 'pali-dict-software-web1version/xml/')
  dstJsonFile = os.path.join(os.path.dirname(__file__), '../gae/libs/json/dicPrefixWordLists.json')

  if not os.path.exists(srcXmlDir):
    print(srcXmlDir + ' does not exist!')
    sys.exit(1)

  if not os.path.exists(os.path.dirname(dstJsonFile)):
    os.makedirs(os.path.dirname(dstJsonFile))

  dicPrefixWordLists = {}

  # iterate all files in directories recursively
  # References:
  # http://stackoverflow.com/questions/2212643/python-recursive-folder-read
  # http://docs.python.org/2/library/os.html#os.walk
  for dirpath, dirnames, filenames in os.walk(srcXmlDir):
    if len(dirnames) != 0:
      continue

    fistCharOfWord = os.path.basename(dirpath).decode('utf-8')
    dicPrefixWordLists[fistCharOfWord] = []

    # iterate all words start with prefix 'fistCharOfWord'
    for filename in filenames:
      srcFilepath = os.path.join(dirpath, filename)
      word = filename[:-4].decode('utf-8')

      # covert word into fuzzy word, example: gaṇakī => ganaki
      fuzzyWord = u""
      # http://stackoverflow.com/questions/538346/iterating-over-a-string-python
      for c in word:
        # http://stackoverflow.com/questions/1602934/what-is-a-good-way-to-test-if-a-key-exists-in-python-dictionary
        if c in fuzzyChars:
          fuzzyWord += fuzzyChars[c]
        else:
          fuzzyWord += c

      if word != fuzzyWord:
        dicPrefixWordLists[fistCharOfWord].append(word)
        continue

      # http://effbot.org/zone/python-with-statement.htm
      with open(srcFilepath, 'r') as f:
        # parse the xml data in the file
        dom = xml.dom.minidom.parseString(f.read())

        # iterate all the 'word' tag inside a xml file
        wordsInXml = dom.getElementsByTagName('word')
        for wordInXml in wordsInXml:
          wordStr = wordInXml.childNodes[0].data
          # FIXME: is lower() safe here?
          if (wordStr.lower() == word):
            # This is a "true" word
            dicPrefixWordLists[fistCharOfWord].append(word)
            break

  # If old json file exists, delete it.
  if os.path.exists(dstJsonFile):
    os.remove(dstJsonFile)

  # sort the words
  for key in dicPrefixWordLists:
    dicPrefixWordLists[key].sort()

  # dicPrefixWordLists = {
  #   "a" : [ ... ]
  #   "ā" : [ ... ],
  #   "b" : [ ... ],
  #   "c" : [ ... ],
  #   ...
  # }

  # save the indexes in JSON-format to file
  with open(dstJsonFile, 'w') as f:
    f.write(json.dumps(dicPrefixWordLists))
