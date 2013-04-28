#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json

with open(os.path.join(os.path.dirname(__file__), 'json/treeviewAll.json'), 'r') as f:
  treeviewData = json.loads(f.read())

with open(os.path.join(os.path.dirname(__file__), 'json/translationInfo.json'), 'r') as f:
  translationInfo = json.loads(f.read())

xmlFilename2PathInfo = {}


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
    if 'action' in result['node']:
      if translationLocale in translationInfo:
        xmlFilename = os.path.basename(result['node']['action'])
        if xmlFilename in translationInfo[translationLocale]['canon']:
          for translatorCode in translationInfo[translationLocale]['canon'][xmlFilename]:
            if translationInfo[translationLocale]['source'][translatorCode][0] == translator.decode('utf-8'):
              return result
    return { 'isValid': False }
  else:
    return result


def recursiveGetPath(node, pathPrefix, xmlFilename):
  path = pathPrefix + '/' + node['subpath']
  if 'action' in node:
    if os.path.basename(node['action']) == xmlFilename:
      return path
  else:
    for child in node['child']:
      result = recursiveGetPath(child, path, xmlFilename)
      if result:
        return result


def xmlFilename2Path(xmlFilename):
  if xmlFilename in xmlFilename2PathInfo:
    return xmlFilename2PathInfo[xmlFilename]

  for child in treeviewData['child']:
    result = recursiveGetPath(child, u'', xmlFilename)
    if result:
      xmlFilename2PathInfo[xmlFilename] = result
      return result

  raise Exception('cannot get path of %s' % xmlFilename)
