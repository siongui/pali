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


def getTranslator(translationLocale, localeXmlTranslation):
  return translationInfo[translationLocale]['source'][ localeXmlTranslation['source'] ][0]


def getLocaleXmlTranslations(translationLocale, xmlFilename):
  localeXmlTranslations = []
  for tmp in translationInfo[translationLocale]['canon'][xmlFilename]:
    localeXmlTranslation = { 'translator': getTranslator(translationLocale, tmp) }
    if 'excerpt' in localeXmlTranslation:
      localeXmlTranslation['excerpt'] = tmp['excerpt']
    localeXmlTranslations.append(localeXmlTranslation)

  return localeXmlTranslations


def getI18nLinksTemplateValues(xmlFilename):
  i18nLinksTmpValue = { 'localeTranslations': [] }
  for translationLocale in translationInfo:
    localeTranslation = { 'translationLocale': translationLocale }
    if xmlFilename in translationInfo[translationLocale]['canon']:
      localeTranslation['localeXmlTranslations'] = \
        getLocaleXmlTranslations(translationLocale, xmlFilename)

    if 'localeXmlTranslations' in localeTranslation:
      i18nLinksTmpValue['localeTranslations'].append(localeTranslation)

  if len(i18nLinksTmpValue['localeTranslations']) > 0:
    i18nLinksTmpValue['xmlFilename'] = xmlFilename
    return i18nLinksTmpValue


def getAllLocalesTranslationsTemplateValues():
  localeTranslations = []
  for translationLocale in translationInfo:
    localeTranslation = { 'translationLocale': translationLocale }
    localeTranslation['translations'] = []
    for xmlFilename in translationInfo[translationLocale]['canon']:
      translation = { 'xmlFilename': xmlFilename }
      translation['translator'] = []
      for localeXmlTranslation in translationInfo[translationLocale]['canon'][xmlFilename]:
        translation['translator'].append(translationInfo[translationLocale]['source'][ localeXmlTranslation['source'] ][0])
      localeTranslation['translations'].append(translation)
    localeTranslations.append(localeTranslation)

  return localeTranslations

