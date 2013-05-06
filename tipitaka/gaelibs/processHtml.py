#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import xml.dom.minidom
from lxml import etree
from xml2html import paliXslt
from xml2html import getCanonXmlUrl
from xml2html import getTranslationXmlUrl
from template import getJinja2Env
from template import getTranslationPageOriPaliLinkHtml
from template import getContrastReadingPageOriPaliLinkHtml
from translationInfo import getI18nLinksTemplateValues


def getBodyDom(xmlUrl):
  # feed transformed data to minidom for processing
  dom = xml.dom.minidom.parseString(etree.tostring(paliXslt(xmlUrl)))
  # return only dom of body
  return dom.documentElement.getElementsByTagName('body')[0]


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


def getTranslationXmlBodyDom(translationLocale, translator, action):
  return getBodyDom(getTranslationXmlUrl(action, translationLocale, translator))


def getTranslationPageHtml(translationLocale, translator, action, reqPath):
  html = getTranslationPageOriPaliLinkHtml(reqPath)
  # return only innerHTML of body
  html += getTranslationXmlBodyDom(translationLocale, translator, action).toxml()[6:-7]
  return html


def generateContrastReadingTable(oriBody, trBody):
  if (len(oriBody.childNodes) != len(trBody.childNodes)):
    raise Exception('two XML document body childs # not match')

  contrastReadings = []
  for i in range(len(oriBody.childNodes)):
    if oriBody.childNodes[i].nodeType != xml.dom.Node.ELEMENT_NODE and \
       trBody.childNodes[i].nodeType != xml.dom.Node.ELEMENT_NODE:
      continue

    contrastReadings.append([oriBody.childNodes[i].toxml(),
                             trBody.childNodes[i].toxml()])

  template = getJinja2Env().get_template('contrastReading.html')
  return template.render({'contrastReadings': contrastReadings })


def getContrastReadingPageHtml(translationLocale, translator, action, reqPath):
  html = getContrastReadingPageOriPaliLinkHtml(reqPath)

  xmlUrl = getCanonXmlUrl(action)
  oriBody= getBodyDom(xmlUrl)
  trBody = getTranslationXmlBodyDom(translationLocale, translator, action)
  html += generateContrastReadingTable(oriBody, trBody)

  return html
