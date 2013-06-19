#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import imp
from lxml import etree

from variables import ftoj
from variables import localedir
from variables import TranslationDir


def getTranslationInfo():
  translationInfo = {}
  langsXml = etree.parse( os.path.join(TranslationDir, 'languages.xml') )

  for language in langsXml.xpath('.//language'):
    # traverse dir with specific language
    directory = language.find('directory')
    lang = directory.text
    translationInfo[lang] = { 'canon': {}, 'source': {} }

    sourcesXml = etree.parse( os.path.join(TranslationDir,
        '%s/sources.xml' % lang) )
    for source in sourcesXml.xpath('.//source'):
      # read informations of translators
      key = source.find('key').text
      translator = source.find('translator').text
      translationInfo[lang]['source'][key] = [ translator ]

      translatorXmlDir = os.path.join( TranslationDir, '%s/%s/' % (lang, key) )
      for xml in os.listdir(translatorXmlDir):
        # traverse dir with translations by specific translator
        if not xml.endswith('.xml'): continue

        xmlInfo = { 'source': key }
        xmlTree = etree.parse( os.path.join(translatorXmlDir, xml) )
        isExcerpt = xmlTree.find('.//excerpt')
        if isExcerpt is not None:
          xmlInfo['excerpt'] = True

        if xml in translationInfo[lang]['canon']:
          translationInfo[lang]['canon'][xml].append( xmlInfo )
        else:
          translationInfo[lang]['canon'][xml] = [ xmlInfo ]

  import pprint
  pprint.pprint(translationInfo)
  return translationInfo


def getCanonTextTranslation():
  canonTextTranslation = {}

  # initialize canonTextTranslation
  for dirpath, dirnames, filenames in os.walk(localedir):
    for dirname in dirnames:
      locale = dirname
      path = os.path.join(localedir, '%s/LC_MESSAGES/PaliTextTitle.py' % locale)
      if os.path.isfile(path):
        var = imp.load_source('PaliTextTitle', path)
        canonTextTranslation[locale] = var.PaliTextTitle
    break

  # derive zh_CN from zh_TW
  canonTextTranslation['zh_CN'] = {}
  for key in canonTextTranslation['zh_TW']:
    canonTextTranslation['zh_CN'][key] = ftoj(canonTextTranslation['zh_TW'][key])

  return canonTextTranslation


if __name__ == '__main__':
  dstTrInfoPath = os.path.join(os.path.dirname(__file__),
      '../pylib/json/translationInfo.json')
  dstCanonTextTranslationPath = os.path.join(os.path.dirname(__file__),
      '../pylib/json/canonTextTranslation.json')

  if not os.path.exists(os.path.dirname(dstTrInfoPath)):
    os.makedirs(os.path.dirname(dstTrInfoPath))

  translationInfo = getTranslationInfo()
  with open(dstTrInfoPath, 'w') as f:
    f.write(json.dumps(translationInfo))

  canonTextTranslation = getCanonTextTranslation()
  with open(dstCanonTextTranslationPath, 'w') as f:
    f.write(json.dumps(canonTextTranslation))

  dstTrServicePath = os.path.join(os.path.dirname(__file__),
      '../app/scripts/services/data/i18nTpk.js')

  if not os.path.exists(os.path.dirname(dstTrServicePath)):
    os.makedirs(os.path.dirname(dstTrServicePath))
  with open(dstTrServicePath, 'w') as f:
    f.write("angular.module('pali.data.i18nTpk', []).\n")
    f.write("  factory('i18nTpk', [function() {\n")
    #f.write("    var translationInfo = ")
    #f.write(json.dumps(translationInfo))
    #f.write(";\n")
    f.write("    var canonTextTranslation = ")
    f.write(json.dumps(canonTextTranslation))
    f.write(";\n")
    f.write("    return { canonTextTranslation: canonTextTranslation };\n")
    #f.write("    var serviceInstance = { translationInfo: translationInfo, canonTextTranslation: canonTextTranslation };\n")
    #f.write("    return serviceInstance;\n")
    f.write("  }]);\n")
