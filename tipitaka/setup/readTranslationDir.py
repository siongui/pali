#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from lxml import etree

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


if __name__ == '__main__':
  for lang, key, translator, xml, isExcerpt in xmlInfo():
    print(lang, key, translator, xml, isExcerpt)
