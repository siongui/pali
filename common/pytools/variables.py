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
