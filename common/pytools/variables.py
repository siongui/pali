#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

def getSDKPath():
  return os.path.join(os.path.dirname(__file__), "../../../google_appengine/")

def getDictBooksCSVPath():
  return os.path.join(os.path.dirname(__file__),
      "../../../data/pali/common/dictionary/dict-books.csv")

def getDictBooksJsonPath():
  return os.path.join(os.path.dirname(__file__),
      "../gae/libs/json/books.json")

def getDictBooksJsPath():
  return os.path.join(os.path.dirname(__file__),
      "../app/scripts/services/data/dicBooks.js")

def getSuccinctTrieJsonPath():
  return os.path.join(os.path.dirname(__file__),
      "../gae/libs/json/succinct_trie.json")

def getSuccinctTrieJsPath():
  return os.path.join(os.path.dirname(__file__),
      "../app/scripts/services/data/succinctTrie.js")

def getLocaleDir():
  return os.path.join(os.path.dirname(__file__), '../locale')

def getDicHtmlDir():
  return os.path.join(os.path.dirname(__file__), '../../dictionary/app')

def getTpkHtmlDir():
  return os.path.join(os.path.dirname(__file__), '../../tipitaka/app')

def getDicHtmlDir2():
  return os.path.join(os.path.dirname(__file__), '../../dictionary/gaelibs/partials')

def getTpkHtmlDir2():
  return os.path.join(os.path.dirname(__file__), '../../tipitaka/gaelibs/partials')

def getPotPath():
  return os.path.join(getLocaleDir(), 'messages.pot')

def getTWPoPath():
  return os.path.join(getLocaleDir(), 'zh_TW/LC_MESSAGES/messages.po')

def getCNPoPath():
  return os.path.join(getLocaleDir(), 'zh_CN/LC_MESSAGES/messages.po')

def getDstLocalesJsPath():
  return os.path.join(os.path.dirname(__file__),
      '../app/scripts/services/data/i18nStrings.js')

