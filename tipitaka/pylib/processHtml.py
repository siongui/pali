#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from lxml import etree
from xml2html import paliXslt
from xml2html import translationXslt
from template import getJinja2Env
from translationInfo import getI18nLinksTemplateValues
from translationInfo import getXmlLocaleTranslationInfo
from footNote import processNotes
from footNote import processTranslatedPElementsNotes


def getCanonPageHtml(node, reqPath, userLocale):
  canonPageTemplateValue = { 'reqPath': reqPath }
  if 'action' in node:
    canonPageTemplateValue['isPaliText'] = True
    # set links of translation and contrast reading if any
    canonPageTemplateValue['i18nLinks'] = \
             getI18nLinksTemplateValues(os.path.basename(node['action']))
    # xslt
    transformedHtml = paliXslt(node['action'])
    # get innerHTML of body
    canonPageTemplateValue['body'] = etree.tostring(
                                      transformedHtml.find('body'))[6:-7]
  else:
    canonPageTemplateValue['childs'] = node['child']

  template = getJinja2Env(userLocale).get_template('canonPage.html')
  return template.render(canonPageTemplateValue);


def getTranslationPageHtml(translationLocale, translator, action,
                           reqPath, userLocale):
  translationPageTemplateValue = {
      'reqPath': reqPath,
      'trInfo': getXmlLocaleTranslationInfo(action,
                                            translationLocale,
                                            translator) }
  # xslt
  transformedHtml = translationXslt(action, translationLocale, translator)
  processNotes(transformedHtml)
  # get innerHTML of body
  translationPageTemplateValue['body'] = etree.tostring(
                                    transformedHtml.find('body'))[6:-7]

  template = getJinja2Env(userLocale).get_template('translationPage.html')
  return template.render(translationPageTemplateValue);


def getContrastReadingPageHtml(translationLocale, translator, action,
                               reqPath, userLocale):
  contrastReadingPageTemplateValue = {
      'reqPath': reqPath,
      'trInfo': getXmlLocaleTranslationInfo(action,
                                            translationLocale,
                                            translator) }

  oriBody = paliXslt(action).find('body')
  trBody = translationXslt(action, translationLocale, translator).find('body')
  if (len(oriBody) != len(trBody)):
    raise Exception('two XML document body childs # not match')

  table = etree.fromstring('<table class="ctReading"></table>')
  trPElms = []
  # create contrast (parallet) reading table
  for i in range(len(oriBody)):
    if oriBody[0].tag != 'p' or trBody[0].tag != 'p':
      raise Exception('not in p tag')

    tr = etree.fromstring('<tr></tr>')
    if etree.tostring(oriBody[0]) == etree.tostring(trBody[0]):
      # not translated
      tdOri = etree.fromstring('<td></td>')
      tdOri.append(oriBody[0])
      tdTr = etree.fromstring('<td></td>')
      trBody.remove(trBody[0])
      tr.append(tdOri)
      tr.append(tdTr)
    else:
      tdOri = etree.fromstring('<td></td>')
      tdOri.append(oriBody[0])
      tdTr = etree.fromstring('<td></td>')
      trPElms.append(trBody[0])
      tdTr.append(trBody[0])
      tr.append(tdOri)
      tr.append(tdTr)

    table.append(tr)

  footNotes = processTranslatedPElementsNotes(trPElms)

  contrastReadingPageTemplateValue['contrastReadings'] = \
    etree.tostring(table) + etree.tostring(footNotes)

  template = getJinja2Env(userLocale).get_template('contrastReadingPage.html')
  return template.render(contrastReadingPageTemplateValue)
