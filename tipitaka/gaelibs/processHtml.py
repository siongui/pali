#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from lxml import etree
from xml2html import paliXslt
from xml2html import translationXslt
from template import getJinja2Env
from translationInfo import getI18nLinksTemplateValues
from translationInfo import getXmlLocaleTranslationInfo


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
  # get innerHTML of body
  translationPageTemplateValue['body'] = etree.tostring(
                                    transformedHtml.find('body'))[6:-7]

  template = getJinja2Env(userLocale).get_template('translationPage.html')
  return template.render(translationPageTemplateValue);


def contrastReadingTemplateValue(oriBody, trBody):
  if (len(oriBody) != len(trBody)):
    raise Exception('two XML document body childs # not match')

  contrastReadings = []
  for i in range(len(oriBody)):
    if oriBody[i].tag != 'p' and \
       trBody[i].tag != 'p':
      continue

    oriHtmlI = etree.tostring(oriBody[i])
    trHtmlI = etree.tostring(trBody[i])
    if oriHtmlI == trHtmlI:
      contrastReadings.append( [ oriHtmlI, '' ] )
    else:
      contrastReadings.append( [ oriHtmlI, trHtmlI ] )

  return contrastReadings


def getContrastReadingPageHtml(translationLocale, translator, action,
                               reqPath, userLocale):
  contrastReadingPageTemplateValue = {
      'reqPath': reqPath,
      'trInfo': getXmlLocaleTranslationInfo(action,
                                            translationLocale,
                                            translator) }
  # xslt
  oriTransformedHtml = paliXslt(action)
  trTransformedHtml = translationXslt(action, translationLocale, translator)

  oriBody = oriTransformedHtml.find('body')
  trBody = trTransformedHtml.find('body')

  contrastReadingPageTemplateValue['contrastReadings'] = \
    contrastReadingTemplateValue(oriBody, trBody)

  template = getJinja2Env(userLocale).get_template('contrastReadingPage.html')
  return template.render(contrastReadingPageTemplateValue)
