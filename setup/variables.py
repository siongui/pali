#!/usr/bin/env python
# -*- coding:utf-8 -*-

from os.path import join
from os.path import dirname

try:
  import pyopencc
  ftoj = pyopencc.OpenCC('zht2zhs.ini').convert
except:
  print('cannot import opencc, import jianfan')
  import sys
  sys.path.append(join(dirname(__file__), '../common/pylib'))
  from jianfan import ftoj

DICTIONARY_DIR = join(dirname(__file__), '../dictionary')
TIPITAKA_DIR = join(dirname(__file__), '../tipitaka')
APP_COMMON_DATA_DIR = join(dirname(__file__),
    "../common/app/scripts/services/data/")

def getSDKPath():
  return join(dirname(__file__), "../../google_appengine/")

def getLocaleDir():
  return join(dirname(__file__), '../common/locale/')

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

