#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import re

with open(os.path.join(os.path.dirname(__file__),
                       'json/canonTextTranslation.json'), 'r') as f:
  canonTextTranslation = json.loads(f.read())


def nodeTextStrip(text):
  string = text

  # remove leading un-needed characters
  match = re.search(r'^[\d\s()-\.]+', string)
  if match:
    string = string[len(match.group()):]

  # remove trailing un-needed characters
  match = re.search(r'-\d$', string)
  if match:
    string = string[:-len(match.group())]

  return string


def nodeTextStrip2(text):
  string = nodeTextStrip(text)

  if string.endswith(u'pāḷi'):
    string = string[:-4]

  if string.endswith(u'nikāya'):
    string = string[:-6]

  if string.endswith(u'piṭaka'):
    string = string[:-6]

  return string


def translateNodeText(text, locale):
  string = nodeTextStrip(text)

  if locale in canonTextTranslation:
    if string in canonTextTranslation[locale]:
      return canonTextTranslation[locale][string]

  return text


def translateNodeText4(text, locale):
  trText = translateNodeText(text, locale)
  if trText == text:
    return nodeTextStrip2(text)
  else:
    return trText


# cache
translatedCanonNameCache = {}

def getTranslatedCanonName(text):
  # check cache first
  if text in translatedCanonNameCache:
    return translatedCanonNameCache[text]

  # cache miss, go find translated names
  trText = {}
  for locale in canonTextTranslation:
    trText[locale] = translateNodeText(text, locale)
    if trText[locale] == text: trText[locale] = ''

  # store translated canon names in cache
  translatedCanonNameCache[text] = trText
  return trText


# FIXME: ugly coding style
from template import getJinja2Env

jj2env = getJinja2Env('en_US')
jj2env.filters['nodeTextStrip2'] = nodeTextStrip2
jj2env.filters['translateNodeText4'] = translateNodeText4


def getHtmlTitle(urlLocale, texts, userLocale,
                 translator=None, contrastReading=None):
  tmpValue = {'urlLocale': urlLocale,
              'texts': texts }
  if translator:
    tmpValue['translator'] = translator.decode('utf-8')
    tmpValue['contrastReading'] = contrastReading

  titleTemplate = getJinja2Env(userLocale).get_template('title.html')
  return titleTemplate.render(tmpValue)
