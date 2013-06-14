#!/usr/bin/env python
# -*- coding:utf-8 -*-

from os.path import join
from os.path import dirname

TIPITAKA_DIR = join(dirname(__file__), '..')
COMMOM_DATA_DIR = join(dirname(__file__), '../../../data/pali/common')

def getSDKPath():
  return join(dirname(__file__), "../../../google_appengine/")

def getRomnDir():
  return join(COMMOM_DATA_DIR, 'romn')

def getInfoFilePath():
  return join(dirname(__file__), '../build/tocsInfo.txt')

def getTreeviewJsonPath():
  return join(dirname(__file__), '../build/treeview.json')

def getTreeviewAllJsonPath():
  return join(TIPITAKA_DIR, 'pylib/json/treeviewAll.json')

def getTreeviewAllJsPath():
  return join(TIPITAKA_DIR, 'app/scripts/services/data/treeviewAll.js')

