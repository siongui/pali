#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from lxml import etree

from constructTranslationTrees import getTranslationTrees


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
    if 'child' in tree:
      ngVar = '%s%d' % (prefix, index)
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
          '<div class="childrenContainer"></div>')
      for translation in tree['translations']:
        childrenContainer.append( etree.fromstring(
            '<div class="item treeNode">%s</div>'
                % translation['translator'] ) )

    container = etree.fromstring('<div></div>')
    container.append(node)
    container.append(childrenContainer)

    return container


if __name__ == '__main__':
  langTrees = getTranslationTrees()

  langHtmls = {}
  for lang in langTrees:
    langHtmls[lang] = translationTreeToHtml(langTrees[lang], None, None, lang)
    print(etree.tostring(langHtmls[lang], pretty_print=True))

  trTreeHtmlPath = os.path.join(os.path.dirname(__file__),
      '../app/partials/trTree.html')
  with open(trTreeHtmlPath, 'w') as f:
    for lang in langHtmls:
      f.write(etree.tostring(langHtmls[lang]))
