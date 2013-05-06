#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from lxml import etree
from xml2html import paliXslt
from xml2html import getCanonXmlUrl
from xml2html import getTranslationXmlUrl
from template import getJinja2Env
from translationInfo import getI18nLinksTemplateValues


def getCanonPageHtml(node, reqPath):
  canonPageTemplateValue = { 'reqPath': reqPath }
  if 'action' in node:
    canonPageTemplateValue['isPaliText'] = True
    # set links of translation and contrast reading if any
    canonPageTemplateValue['i18nLinks'] = \
             getI18nLinksTemplateValues(os.path.basename(node['action']))
    # xslt
    transformedHtml = paliXslt(getCanonXmlUrl(node['action']))
    # get innerHTML of body
    canonPageTemplateValue['body'] = etree.tostring(
                                      transformedHtml.find('body'))[6:-7]
  else:
    canonPageTemplateValue['childs'] = node['child']

  template = getJinja2Env().get_template('canonPage.html')
  return template.render(canonPageTemplateValue);


def getTranslationPageHtml(translationLocale, translator, action, reqPath):
  translationPageTemplateValue = { 'reqPath': reqPath }
  # xslt
  transformedHtml = paliXslt(getTranslationXmlUrl(
                               action, translationLocale, translator))
  # get innerHTML of body
  translationPageTemplateValue['body'] = etree.tostring(
                                    transformedHtml.find('body'))[6:-7]

  template = getJinja2Env().get_template('translationPage.html')
  return template.render(translationPageTemplateValue);


def contrastReadingTemplateValue(oriBody, trBody):
  if (len(oriBody) != len(trBody)):
    raise Exception('two XML document body childs # not match')

  contrastReadings = []
  for i in range(len(oriBody)):
    if oriBody[i].tag != 'p' and \
       trBody[i].tag != 'p':
      continue

    contrastReadings.append([etree.tostring(oriBody[i]),
                             etree.tostring(trBody[i]) ])

  return contrastReadings


def getContrastReadingPageHtml(translationLocale, translator, action, reqPath):
  contrastReadingPageTemplateValue = { 'reqPath': reqPath }
  # xslt
  oriTransformedHtml = paliXslt(getCanonXmlUrl(action))
  trTransformedHtml = paliXslt(getTranslationXmlUrl(
                               action, translationLocale, translator))

  oriBody = oriTransformedHtml.find('body')
  trBody = trTransformedHtml.find('body')

  contrastReadingPageTemplateValue['contrastReadings'] = \
    contrastReadingTemplateValue(oriBody, trBody)

  template = getJinja2Env().get_template('contrastReadingPage.html')
  return template.render(contrastReadingPageTemplateValue)
