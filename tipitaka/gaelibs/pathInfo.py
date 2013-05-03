#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json

# http://stackoverflow.com/questions/3898572/what-is-the-standard-python-docstring-format
# http://stackoverflow.com/questions/2447109/showing-a-different-background-colour-in-vim-past-80-characters
"""format of variable in treeviewAll.json

The variable in treeviewAll.json is a Python dict (JavaScript object) which is:
    { tipitakaNode, atthakathaNode, tikaNode, anyaNode }
where each node contains the following attribute:
    Non-leaf node:
        { 'text': string ,
          'child': [ node, node, ... ],
          'subpath': string }
    Leaf node:
        { 'text': string ,
          'action': string,
          'subpath': string }
This is a tree structure.
"""
with open(os.path.join(os.path.dirname(__file__), 'json/treeviewAll.json'), 'r') as f:
  treeviewData = json.loads(f.read())

# See translationInfo.py
with open(os.path.join(os.path.dirname(__file__), 'json/translationInfo.json'), 'r') as f:
  translationInfo = json.loads(f.read())

# cache of {xmlFilename, paliTextPath} pairs
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
  """Check if the path of URL is valid.

  The path of URL could be one of the following:
      {{paliText}}
      /{{urlLocale}}{{paliTextPath}}
      /{{urlLocale}}{{paliTextPath}}/{{translationLocale}}/{{translator}}
      /{{urlLocale}}{{paliTextPath}}/{{translationLocale}}/{{translator}}/ContrastReading
  Before the path is being passed in this function, it has already been filtered
  by Python web framework like webapp2 or web.py, so {{urlLocale}} has been
  stripped.

  Args:
      paliTextPath: for example:
          /canon
          /canon/sutta
          /canon/sutta/dīgha
          /canon/sutta/dīgha/sīlakkhandhavagga
          /canon/sutta/dīgha/sīlakkhandhavagga/sāmaññaphalasuttaṃ

      translationLocale: particular language translation of pali text of
          {{paliTextPath}}, for example:
          en_US: English translation of pali text of {{paliTextPath}}
          zh_TW: Traditional Chinese translation of pali text of 
              {{paliTextPath}}

      translator: name of the translator

  Returns:
      A dict which contains the following information if the path is valid:

       { 'isValid': True,
         'node': one of the node of the variable in treeviewAll.json,
                 which corresponds to {{paliTextPath}},
         'texts': [ node1['text'], ... ] }

      If not valid path, return { 'isValid': False }
  """
  result = isValidPaliTextPath(paliTextPath)
  if result['isValid'] and translationLocale:
    if 'action' in result['node']:
      if translationLocale in translationInfo:
        xmlFilename = os.path.basename(result['node']['action'])
        if xmlFilename in translationInfo[translationLocale]['canon']:
          for localeXmlTranslation in translationInfo[translationLocale]['canon'][xmlFilename]:
            if translationInfo[translationLocale]['source'][ localeXmlTranslation['source'] ][0] == translator.decode('utf-8'):
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
