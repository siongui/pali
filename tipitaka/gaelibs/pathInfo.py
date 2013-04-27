#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json

with open(os.path.join(os.path.dirname(__file__), 'json/treeviewAll.json'), 'r') as f:
  treeviewData = json.loads(f.read())


def isValidPath(paliTextPath, translationLocale=None, translator=None):
  pass
