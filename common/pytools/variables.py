#!/usr/bin/env python
# -*- coding:utf-8 -*-

from os.path import join
from os.path import dirname

DICTIONARY_DIR = join(dirname(__file__), '../../dictionary')
TIPITAKA_DIR = join(dirname(__file__), '../../tipitaka')
COMMOM_DATA_DIR = join(dirname(__file__), '../../../data/pali/common')
APP_COMMON_DATA_DIR = join(dirname(__file__), "../app/scripts/services/data")

def getSDKPath():
  return join(dirname(__file__), "../../../google_appengine/")

def getRomnDir():
  return join(COMMOM_DATA_DIR, 'romn')

def getDictBooksCSVPath():
  return join(COMMOM_DATA_DIR, 'dictionary/dict-books.csv')

def getDictWordsCSV1Path():
  return join(COMMOM_DATA_DIR, 'dictionary/dict_words_1.csv')

def getDictWordsCSV2Path():
  return join(COMMOM_DATA_DIR, 'dictionary/dict_words_2.csv')

def getDictWordsJsonDir():
  return join(DICTIONARY_DIR, 'gaelibs/paliwords')

def getPrefixWordsHtmlDir():
  return join(DICTIONARY_DIR, 'gaelibs/prefixWordsHtml')

def getDictBooksJsonPath():
  return join(DICTIONARY_DIR, 'gaelibs/json/books.json')

def getDictBooksJsPath():
  return join(APP_COMMON_DATA_DIR, "dicBooks.js")

def getSuccinctTrieJsonPath():
  return join(DICTIONARY_DIR, 'gaelibs/json/succinct_trie.json')

def getSuccinctTrieJsPath():
  return join(APP_COMMON_DATA_DIR, "succinctTrie.js")

def getLocaleDir():
  return join(dirname(__file__), '../locale')

def getDicHtmlDir():
  return join(DICTIONARY_DIR, 'app')

def getTpkHtmlDir():
  return join(TIPITAKA_DIR, 'app')

def getDicHtmlDir2():
  return join(DICTIONARY_DIR, 'gaelibs/partials')

def getTpkHtmlDir2():
  return join(TIPITAKA_DIR, 'gaelibs/partials')

def getPotPath():
  return join(getLocaleDir(), 'messages.pot')

def getDstLocalesJsPath():
  return join(APP_COMMON_DATA_DIR, "i18nStrings.js")

def getInfoFilePath():
  return join(dirname(__file__), 'tocsInfo.txt')

def getTreeviewJsonPath():
  return join(dirname(__file__), 'treeview.json')

def getTreeviewAllJsonPath():
  return join(TIPITAKA_DIR, 'gaelibs/json/treeviewAll.json')

def getTreeviewAllJsPath():
  return join(TIPITAKA_DIR, 'app/scripts/services/data/treeviewAll.js')

