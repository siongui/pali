#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
from lxml import etree

from variables import TreeviewJsonPath
from variables import TranslationDir

def xmlInfo():
  langsXml = etree.parse( os.path.join(TranslationDir, 'languages.xml') )

  for language in langsXml.xpath('.//language'):
    # traverse dir with specific language
    directory = language.find('directory')
    lang = directory.text

    sourcesXml = etree.parse( os.path.join(TranslationDir,
        '%s/sources.xml' % lang) )
    for source in sourcesXml.xpath('.//source'):
      # read informations of translators
      key = source.find('key').text
      translator = source.find('translator').text

      translatorXmlDir = os.path.join( TranslationDir, '%s/%s/' % (lang, key) )
      for xml in os.listdir(translatorXmlDir):
        # traverse dir with translations by specific translator
        if not xml.endswith('.xml'): continue

        yield (lang, key, translator, xml)


def trimTree(tree):
  keepList = []

  for child in tree['child']:
    if 'keep' in child:
      keepList.append(child)
      if 'child' in child:
        trimTree(child)

  tree['child'] = keepList

def recursiveSetXMLPath(node, xmlFilename):
  if 'action' in node:
    if os.path.basename(node['action']) == xmlFilename:
      node['keep'] = True
      return True
  else:
    for child in node['child']:
      if recursiveSetXMLPath(child, xmlFilename):
        node['keep'] = True
        return True

def getTranslationTree():
  with open(TreeviewJsonPath, 'r') as f:
    treeviewData = json.loads(f.read())

  for lang, key, translator, xmlFilename in xmlInfo():
    print(lang, key, translator, xmlFilename)
    recursiveSetXMLPath(treeviewData, xmlFilename)

  trimTree(treeviewData)
  return treeviewData


def translationTreeToHtml(tree):
  if 'text' not in tree:
    # root tree
    root = etree.fromstring('<div></div>')
    for child in tree['child']:
      root.append( translationTreeToHtml(child) )
    return root
  else:
    node = etree.fromstring('<div class="item"></div>')
    if 'child' in tree:
      sign = etree.fromstring('<span>+</span>')
      textElm = etree.fromstring(
          '<span class="treeNode">%s<br /></span>' % tree['text']
      )

      node.append(sign)
      node.append(textElm)

      for child in tree['child']:
        node.append( translationTreeToHtml(child) )
    else:
      textElm = etree.fromstring(
          '<span class="treeNode">%s<br /></span>' % tree['text']
      )
      node.append(textElm)

    return node


if __name__ == '__main__':
  trTree = getTranslationTree()

  #import pprint
  #pprint.pprint(trTree)

  root = translationTreeToHtml(trTree)
  print(etree.tostring(root, pretty_print=True))
