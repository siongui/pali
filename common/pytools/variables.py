#!/usr/bin/env python
# -*- coding:utf-8 -*-

from os.path import join
from os.path import dirname

DICTIONARY_DIR = join(dirname(__file__), '../../dictionary')
TIPITAKA_DIR = join(dirname(__file__), '../../tipitaka')
APP_COMMON_DATA_DIR = join(dirname(__file__), "../app/scripts/services/data")

def getLocaleDir():
  return join(dirname(__file__), '../locale')

def getDicHtmlDir():
  return join(DICTIONARY_DIR, 'app')

def getTpkHtmlDir():
  return join(TIPITAKA_DIR, 'app')

def getDicHtmlDir2():
  return join(DICTIONARY_DIR, 'pylib/partials')

def getTpkHtmlDir2():
  return join(TIPITAKA_DIR, 'pylib/partials')

def getPotPath():
  return join(getLocaleDir(), 'messages.pot')

def getDstLocalesJsPath():
  return join(APP_COMMON_DATA_DIR, "i18nStrings.js")

