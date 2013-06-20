#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import imp

from variables import ftoj
from variables import localedir

from readTranslationDir import xmlInfo
from translationTreesToHtml import createTranslationTreesHtml

def getTranslationInfo():
  translationInfo = {}
  for lang, key, translator, xml, isExcerpt in xmlInfo():
    print(lang, key, translator, xml, isExcerpt)

    if lang not in translationInfo:
      translationInfo[lang] = { 'canon': {}, 'source': {} }

    if key not in translationInfo[lang]['source']:
      translationInfo[lang]['source'][key] = [ translator ]

    info = { 'source': key }
    if isExcerpt:
      info['excerpt'] = True

    if xml in translationInfo[lang]['canon']:
      translationInfo[lang]['canon'][xml].append( info )
    else:
      translationInfo[lang]['canon'][xml] = [ info ]

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
  createTranslationTreesHtml()

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
