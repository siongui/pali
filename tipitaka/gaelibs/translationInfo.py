#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json

# See setTranslationData.py
with open(os.path.join(os.path.dirname(__file__), 'json/translationInfo.json'), 'r') as f:
  translationInfo = json.loads(f.read())


def isValidTranslation(xmlFilename, translationLocale, translator):
  if translationLocale in translationInfo:
    if xmlFilename in translationInfo[translationLocale]['canon']:
      for localeXmlTranslation in translationInfo[translationLocale]['canon'][xmlFilename]:
        if translationInfo[translationLocale]['source'][ localeXmlTranslation['source'] ][0] == translator.decode('utf-8'):
          return True

  return False


def getTranslatorSource(xmlFilename, translationLocale, translator):
  if xmlFilename in translationInfo[translationLocale]['canon']:
    for localeXmlTranslation in translationInfo[translationLocale]['canon'][xmlFilename]:
      if translationInfo[translationLocale]['source'][ localeXmlTranslation['source'] ][0] == translator.decode('utf-8'):
        code = localeXmlTranslation['source']
        break
    try:
      code
    except:
      raise Exception('cannot find localeXmlTranslation["source"]')
  else:
    raise Exception("%s not in translationInfo[%s]['canon']" % (xmlFilename, locale))

  return code
