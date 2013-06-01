#!/usr/bin/env python
# -*- coding:utf-8 -*-

from variables import getDictBooksJsonPath
from variables import getDictBooksJsPath
from variables import getSuccinctTrieJsonPath
from variables import getSuccinctTrieJsPath

def toAngularJSModule(jsonPath, jsPath):
  with open(jsPath, 'w') as f:
    f.write("angular.module('pali.dicBooks', []).\n")
    f.write("  factory('dicBooks', [function() {\n")
    f.write("    return { dicIndex: ")
    with open(jsonPath, 'r') as f2:
      f.write(f2.read())
    f.write("           };\n")
    f.write("  }]);\n")

def toAngularJSModule2(jsonPath, jsPath):
  with open(jsPath, 'w') as f:
    f.write("angular.module('pali.succinctTrie', []).\n")
    f.write("  factory('succinctTrie', [function() {\n")
    f.write("    return { data: ")
    with open(jsonPath, 'r') as f2:
      f.write(f2.read())
    f.write("           };\n")
    f.write("  }]);\n")

if __name__ == '__main__':
  toAngularJSModule(getDictBooksJsonPath(), getDictBooksJsPath())
  toAngularJSModule2(getSuccinctTrieJsonPath(), getSuccinctTrieJsPath())
