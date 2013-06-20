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

        xmlTree = etree.parse( os.path.join(translatorXmlDir, xml) )
        isExcerpt = False
        if xmlTree.find('.//excerpt') is not None:
          isExcerpt = True

        yield (lang, key, translator, xml, isExcerpt)


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

def getTranslationTree():
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


def translationTreeToHtml(tree, prefix, index, locale):
  if 'text' not in tree:
    # root tree
    ngVar = "show%s" % locale

    root = etree.fromstring('<div ng-init="%s = true"></div>' % ngVar)

    textContainer = etree.fromstring(
        '<div ng-click="%s = !%s" class="item treeNode"></div>'
         % (ngVar, ngVar) )
    textContainer.append(
        etree.fromstring('<span ng-show="%s">+</span>' % ngVar) )
    textContainer.append(
        etree.fromstring('<span ng-hide="%s">-</span>' % ngVar) )
    textContainer.append(
        etree.fromstring('<span> </span>') )
    textContainer.append(
        etree.fromstring('<span>{{ "%s" | translate }}</span>' % locale) )
    textContainer.append(
        etree.fromstring('<span> </span>') )
    textContainer.append(
        etree.fromstring('<span>{{_("Translation")}}</span>') )

    root.append(textContainer)

    childrenContainer = etree.fromstring(
        '<div ng-hide="%s" class="childrenContainer"></div>' % ngVar)
    childIndex = 0
    for child in tree['child']:
      childrenContainer.append( translationTreeToHtml(
          child, '%sng' % locale, childIndex, locale) )
      childIndex += 1

    root.append(childrenContainer)
    return root

  else:
    ngVar = '%s%d' % (prefix, index)

    if 'child' in tree:
      node = etree.fromstring(
          '<div ng-init="%s = true" ng-click="%s = !%s" class="item"></div>'
          % (ngVar, ngVar, ngVar) )
      signp = etree.fromstring('<span ng-show="%s">+</span>' % ngVar)
      signm = etree.fromstring('<span ng-hide="%s">-</span>' % ngVar)
      textElm = etree.fromstring(
          '<span class="treeNode">%s<br /></span>' % tree['text'])

      node.append(signp)
      node.append(signm)
      node.append(textElm)

      childrenContainer = etree.fromstring(
          '<div ng-hide="%s" class="childrenContainer"></div>' % ngVar)
      childIndex = 0
      for child in tree['child']:
        childrenContainer.append(
            translationTreeToHtml(child, ngVar, childIndex, locale) )
        childIndex += 1

    else:
      node = etree.fromstring('<div class="item"></div>')
      textElm = etree.fromstring(
          '<span class="treeNode">%s<br /></span>' % tree['text'])
      node.append(textElm)

      childrenContainer = etree.fromstring(
          '<div ng-hide="%s" class="childrenContainer"></div>' % ngVar)
      for translation in tree['translations']:
        childrenContainer.append( etree.fromstring(
            '<div class="item treeNode">%s</div>'
                % translation['translator'] ) )

    container = etree.fromstring('<div></div>')
    container.append(node)
    container.append(childrenContainer)

    return container


if __name__ == '__main__':
  langTrees = getTranslationTree()

  langHtmls = {}
  for lang in langTrees:
    langHtmls[lang] = translationTreeToHtml(langTrees[lang], None, None, lang)
    print(etree.tostring(langHtmls[lang], pretty_print=True))

  trTreeHtmlPath = os.path.join(os.path.dirname(__file__),
      '../app/partials/trTree.html')
  with open(trTreeHtmlPath, 'w') as f:
    for lang in langHtmls:
      f.write(etree.tostring(langHtmls[lang]))
