#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import collections

# See setTranslationData.py
with open(os.path.join(os.path.dirname(__file__), 'json/translationInfo.json'), 'r') as f:
  d = json.JSONDecoder(object_pairs_hook = collections.OrderedDict)
  translationInfo = d.decode(f.read())


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
        return localeXmlTranslation['source']

  raise Exception('cannot find translator source %s %s %s' % (xmlFilename, translationLocale, translator))


def getTranslator(translationLocale, localeXmlTranslation):
  return translationInfo[translationLocale]['source'][ localeXmlTranslation['source'] ][0]


def getLocaleXmlTranslations(translationLocale, xmlFilename):
  localeXmlTranslations = []
  for localeXmlTranslation in translationInfo[translationLocale]['canon'][xmlFilename]:
    tmp = { 'source': localeXmlTranslation['source'],
            'translator': getTranslator(translationLocale, localeXmlTranslation) }

    # check if only partial translation is available
    if 'excerpt' in localeXmlTranslation:
      tmp['excerpt'] = localeXmlTranslation['excerpt']

    localeXmlTranslations.append(tmp)

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

