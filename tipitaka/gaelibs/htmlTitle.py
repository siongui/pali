#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json, re

with open(os.path.join(os.path.dirname(__file__), 'json/canonTextTranslation.json'), 'r') as f:
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


def getHtmlTitle(urlLocale, texts, translator=None, contrastReading=None, i18n=None):
  title = u''

  if texts:
    for text in reversed(texts):
      if urlLocale:
        trText = translateNodeText(text, urlLocale)
        if trText == text:
          title += nodeTextStrip2(text) + u' - '
        else:
          title += trText + u' - '
      else:
        title += nodeTextStrip2(text) + u' - '

  if translator:
    title = translator.decode('utf-8') + u' ' + i18n.gettext(u'Translation')  + u' - ' + title
    if contrastReading:
      title = i18n.gettext(u'Contrast Reading') + u' - ' + title

  return title
