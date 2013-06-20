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


def getChildren(node, ngVar, locale):
  container = etree.fromstring(
      '<div ng-hide="%s" class="childrenContainer"></div>' % ngVar)

  index = 0
  for child in node['child']:
    container.append( translationTreeToHtml(child, ngVar, index, locale) )
    index += 1

  return container

def translationTreeToHtml(tree, prefix, index, locale):
  if 'text' not in tree:
    # root tree
    ngVar = "%sng" % locale

    template = jj2env.get_template('rootNode.html')
    root = etree.fromstring(
        template.render( {'ngVar': ngVar, 'locale': locale } ) )
    root.append( getChildren(tree, ngVar, locale) )
    return root

  else:
    if 'child' in tree:
      ngVar = '%s%d' % (prefix, index)

      template = jj2env.get_template('nonLeafNode.html')
      node = etree.fromstring(
          template.render( {'ngVar': ngVar, 'text': tree['text'] } ) )
      node.append( getChildren(tree, ngVar, locale) )
      return node

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
