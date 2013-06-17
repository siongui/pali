#!/usr/bin/env python
# -*- coding:utf-8 -*-

from os.path import join
from os.path import dirname

try:
  import pyopencc
  jtof = pyopencc.OpenCC('zhs2zht.ini').convert
except:
  print('cannot import opencc, import jianfan')
  import sys
  sys.path.append(join(dirname(__file__), '../common/pylib'))
  from jianfan import jtof

#jtof = lambda x: x

DICTIONARY_DIR = join(dirname(__file__), '..')
DATA_REPO_DIR = join(dirname(__file__), '../../../data/')
APP_COMMON_DATA_DIR = join(dirname(__file__),
    "../../common/app/scripts/services/data/")

def getSDKPath():
  return join(dirname(__file__), "../../../google_appengine/")

def getDictBooksCSVPath():
  return join(DATA_REPO_DIR, 'dictionary/dict-books.csv')

def getDictWordsCSV1Path():
  return join(DATA_REPO_DIR, 'dictionary/dict_words_1.csv')

def getDictWordsCSV2Path():
  return join(DATA_REPO_DIR, 'dictionary/dict_words_2.csv')

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

