#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import jinja2
from lxml import etree

from constructTranslationTrees import getTranslationTrees

jj2env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
      [os.path.join(os.path.dirname(__file__), 'partials')]),
    variable_start_string='{$',
    variable_end_string='$}')


def translationTreeToHtml(tree, prefix, index, locale):
  if 'text' not in tree:
    # root tree
    ngVar = "show%s" % locale

    template = jj2env.get_template('rootNode.html')
    root = etree.fromstring(
        template.render( {'ngVar': ngVar, 'locale': locale } ) )

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

      template = jj2env.get_template('nonLeafNode.html')
      node = etree.fromstring(
          template.render( {'ngVar': ngVar, 'text': tree['text'] } ) )

      childrenContainer = etree.fromstring(
          '<div ng-hide="%s" class="childrenContainer"></div>' % ngVar)
      childIndex = 0
      for child in tree['child']:
        childrenContainer.append(
            translationTreeToHtml(child, ngVar, childIndex, locale) )
        childIndex += 1

      container = etree.fromstring('<div></div>')
      container.append(node)
      container.append(childrenContainer)

      return container

    else:
      template = jj2env.get_template('leafNode.html')
      node = etree.fromstring( template.render(
          {'translations': tree['translations'], 'text': tree['text'] } ) )

      return node


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
