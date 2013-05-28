#!/usr/bin/env python
# -*- coding:utf-8 -*-

from variables import getDictBooksJsonPath
from variables import getDictBooksJsPath

def toAngularJSModule(jsonPath, jsPath):
  with open(jsPath, 'w') as f:
    f.write("angular.module('pali.dicBooks', []).\n")
    f.write("  factory('dicBooks', [function() {\n")
    f.write("    return { dicIndex: ")
    with open(jsonPath, 'r') as f2:
      f.write(f2.read())
    f.write("           };\n")
    f.write("  }]);\n")

if __name__ == '__main__':
  toAngularJSModule(getDictBooksJsonPath(), getDictBooksJsPath())
