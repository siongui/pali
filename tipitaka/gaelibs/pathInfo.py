#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json

with open(os.path.join(os.path.dirname(__file__), 'json/treeviewAll.json'), 'r') as f:
  treeviewData = json.loads(f.read())


def recursivelyCheckPaliTextPath(node, subpathes):
  if len(subpathes) == 0:
    return { 'isValid': False }

  if node['subpath'] == subpathes[0].decode('utf-8'):
    if len(subpathes) == 1:
      return { 'node': node, 'texts': [], 'isValid': True }
    else:
      if 'child' in node:
        for child in node['child']:
          result = recursivelyCheckPaliTextPath(child, subpathes[1:])
          if result['isValid']:
            result['texts'].append(child['text'])
            return result

  return { 'isValid': False }


def isValidPaliTextPath(paliTextPath):
  subpathes = paliTextPath.split('/')
  if subpathes[0] != '':
    raise Exception('illegal paliTextPath: %s' % paliTextPath)
  else:
    subpathes = subpathes[1:]

  for rootNode in treeviewData['child']:
    result = recursivelyCheckPaliTextPath(rootNode, subpathes)
    if result['isValid']:
      result['texts'].append(rootNode['text'])
      return result

  return { 'isValid': False }


def isValidPath(paliTextPath, translationLocale=None, translator=None):
  result = isValidPaliTextPath(paliTextPath)
  if result['isValid'] and translationLocale:
    # TODO: check translationLocale and translator here
    pass

  return result
