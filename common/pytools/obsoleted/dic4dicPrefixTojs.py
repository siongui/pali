#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys, shutil
import json


def toAngularJSModule(dicPrefixWordLists, dicPrefixGroup, path):
  with open(path, 'w') as f:
    f.write("angular.module('pali.dicPrefix', []).\n")
    f.write("  factory('dicPrefix', [function() {\n")
    f.write("    var dicPrefixWordLists = ")
    f.write(json.dumps(dicPrefixWordLists))
    f.write(";\n")
    f.write("    var dicPrefixGroup = ")
    f.write(json.dumps(dicPrefixGroup))
    f.write(";\n")
    f.write("    var serviceInstance = { WordLists: dicPrefixWordLists, Group: dicPrefixGroup };\n")
    f.write("    return serviceInstance;\n")
    f.write("  }]);\n")


if __name__ == '__main__':
  srcJsonFile1 = os.path.join(os.path.dirname(__file__), '../gae/libs/json/dicPrefixWordLists.json')
  srcJsonFile2 = os.path.join(os.path.dirname(__file__), '../gae/libs/json/dicPrefixGroup.json')
  dstJsFile = os.path.join(os.path.dirname(__file__), '../app/js/dicPrefix.js')
  dstAngularFile = os.path.join(os.path.dirname(__file__), '../app/js/services-dicPrefix.js')

  if not os.path.exists(srcJsonFile1):
    print(srcJsonFile1 + ' does not exist!')
    sys.exit(1)

  if not os.path.exists(srcJsonFile2):
    print(srcJsonFile2 + ' does not exist!')
    sys.exit(1)

  with open(srcJsonFile1, 'r') as f:
    dicPrefixWordLists = json.loads(f.read())

  with open(srcJsonFile2, 'r') as f:
    dicPrefixGroup = json.loads(f.read())

  """
  with open(dstJsFile, 'w') as f:
    f.write('var dicPrefixWordLists = ')
    f.write(json.dumps(dicPrefixWordLists))
    f.write(';\n')
    f.write('var dicPrefixGroup = ')
    f.write(json.dumps(dicPrefixGroup))
    f.write(';\n')
  """

  toAngularJSModule(dicPrefixWordLists, dicPrefixGroup, dstAngularFile)
