#!/usr/bin/env python
# -*- coding:utf-8 -*-

from os.path import join
from os.path import dirname

DICTIONARY_DIR = join(dirname(__file__), '..')
COMMOM_DATA_DIR = join(dirname(__file__), '../../../data/pali/common')
APP_COMMON_DATA_DIR = join(dirname(__file__),
    "../../common/app/scripts/services/data/")

def isZhTW():
  return True

def getSDKPath():
  return join(dirname(__file__), "../../../google_appengine/")

def getDictBooksCSVPath():
  return join(COMMOM_DATA_DIR, 'dictionary/dict-books.csv')

def getDictWordsCSV1Path():
  return join(COMMOM_DATA_DIR, 'dictionary/dict_words_1.csv')

def getDictWordsCSV2Path():
  return join(COMMOM_DATA_DIR, 'dictionary/dict_words_2.csv')

def getDictWordsJsonDir():
  return join(DICTIONARY_DIR, 'pylib/paliwords')

def getPrefixWordsHtmlDir():
  return join(DICTIONARY_DIR, 'pylib/prefixWordsHtml')

def getDictBooksJsonPath():
  return join(DICTIONARY_DIR, 'pylib/json/books.json')

def getDictBooksJsPath():
  return join(APP_COMMON_DATA_DIR, "dicBooks.js")

def getSuccinctTrieJsonPath():
  return join(DICTIONARY_DIR, 'pylib/json/succinct_trie.json')

def getSuccinctTrieJsPath():
  return join(APP_COMMON_DATA_DIR, "succinctTrie.js")

