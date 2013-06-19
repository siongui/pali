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

TIPITAKA_DIR = join(dirname(__file__), '..')
DATA_REPO_DIR = join(dirname(__file__), '../../../data/')

localedir = join(dirname(__file__), '../../common/locale/')

TranslationDir = join(DATA_REPO_DIR, 'tipitaka/translation/')
TreeviewJsonPath = join(dirname(__file__), '../build/treeview.json')

def getSDKPath():
  return join(dirname(__file__), "../../../google_appengine/")

def getRomnDir():
  return join(DATA_REPO_DIR, 'tipitaka/romn/')

def getInfoFilePath():
  return join(dirname(__file__), '../build/tocsInfo.txt')

def getTreeviewJsonPath():
  return join(dirname(__file__), '../build/treeview.json')

def getTreeviewAllJsonPath():
  return join(TIPITAKA_DIR, 'pylib/json/treeviewAll.json')

def getTreeviewAllJsPath():
  return join(TIPITAKA_DIR, 'app/scripts/services/data/treeviewAll.js')

