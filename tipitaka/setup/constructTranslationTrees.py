#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json

from variables import TreeviewJsonPath
from readTranslationDir import xmlInfo


def trimTree(tree):
  keepList = []

  for child in tree['child']:
    if 'keep' in child:
      keepList.append(child)
      if 'child' in child:
        trimTree(child)

  tree['child'] = keepList


def recursiveSetXMLPath(node, xmlFileInfo):
  if 'action' in node:
    if os.path.basename(node['action']) == xmlFileInfo[2]:
      node['keep'] = True

      if 'translations' in node:
        node['translations'].append( {'key': xmlFileInfo[0],
                                      'translator': xmlFileInfo[1],
                                      'xmlFilename': xmlFileInfo[2],
                                      'isExcerpt': xmlFileInfo[3] } )
      else:
        node['translations'] = [ {'key': xmlFileInfo[0],
                                  'translator': xmlFileInfo[1],
                                  'xmlFilename': xmlFileInfo[2],
                                  'isExcerpt': xmlFileInfo[3] } ]

      return True
  else:
    for child in node['child']:
      if recursiveSetXMLPath(child, xmlFileInfo):
        node['keep'] = True
        return True


def getTranslationTrees():
  langTrees = {}

  for lang, key, translator, xmlFilename, isExcerpt in xmlInfo():
    print(lang, key, translator, xmlFilename, isExcerpt)

    if lang not in langTrees:
      with open(TreeviewJsonPath, 'r') as f:
        langTrees[lang] = json.loads(f.read())

    recursiveSetXMLPath(langTrees[lang],
                        [key, translator, xmlFilename, isExcerpt])

  for lang in langTrees:
    trimTree(langTrees[lang])

  return langTrees


if __name__ == '__main__':
  langTrees = getTranslationTrees()

  try:
    import pprint
    for lang in langTrees:
      pprint.pprint(langTrees[lang])
  except ImportError:
    pass
