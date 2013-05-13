#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json
# from translationInfo import isValidTranslation (cannot use because of circular import)
import translationInfo
from htmlTitle import nodeTextStrip2
from htmlTitle import getTranslatedCanonName

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
with open(os.path.join(os.path.dirname(__file__), 
                       'json/treeviewAll.json' ), 'r') as f:
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
  """Check if the path of URL is valid.

  The path of URL could be one of the following:
      {{paliText}}
      /{{urlLocale}}{{paliTextPath}}
      /{{urlLocale}}{{paliTextPath}}/{{translationLocale}}/{{translator}}
      /{{urlLocale}}{{paliTextPath}}/{{translationLocale}}/{{translator}}/ContrastReading
  Before this function is called, the path has already been parsed by Python
  web framework like webapp2 or web.py, so {{urlLocale}} has been stripped.

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

      translator: the name of the translator

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
      xmlFilename = os.path.basename(result['node']['action'])
      if translationInfo.isValidTranslation(xmlFilename, translationLocale, translator):
        return result
    return { 'isValid': False }
  else:
    return result


def recursiveGetInfo(node, pathPrefix, xmlFilename):
  path = pathPrefix + '/' + node['subpath']
  if 'action' in node:
    if os.path.basename(node['action']) == xmlFilename:
      return { 'path': path,
               'canonNames': [nodeTextStrip2(node['text'])],
               'translatedCanonNames': [getTranslatedCanonName(node['text'])] }
  else:
    for child in node['child']:
      result = recursiveGetInfo(child, path, xmlFilename)
      if result:
        result['canonNames'].append(nodeTextStrip2(node['text']))
        result['translatedCanonNames'].append(getTranslatedCanonName(node['text']))
        return result

# cache
xmlFilename2InfoCache = {}

def xmlFilename2Info(xmlFilename):
  """Convert xmlFilename to corresponding information.

  Args:
      xmlFilename: the name of the xml file of pali text, for example:
          s0102m.mul2.xml
          s0402m2.mul6.xml

  Returns:
      The corresponding information.
          { 'path': {{paliTextPath}},
            'canonNames': canonNames,
            'translatedCanonNames': translatedCanonNames }
  """
  if xmlFilename in xmlFilename2InfoCache:
    return xmlFilename2InfoCache[xmlFilename]

  for child in treeviewData['child']:
    result = recursiveGetInfo(child, u'', xmlFilename)
    if result:
      xmlFilename2InfoCache[xmlFilename] = result
      return result

  raise Exception('cannot get info of %s' % xmlFilename)
