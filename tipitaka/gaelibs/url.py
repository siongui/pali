#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from lxml import etree
import xml.dom.minidom
from translationInfo import getI18nLinksTemplateValues
from translationInfo import getAllLocalesTranslationsTemplateValues
from template import getJinja2Env
from template import getTranslationPageOriPaliLinkHtml
from template import getContrastReadingPageOriPaliLinkHtml
from pathInfo import isValidPath
from htmlTitle import getHtmlTitle
from xml2html import paliXslt
from xml2html import getCanonXmlUrl
from xml2html import getTranslationXmlUrl


def checkPath(reqPath, urlLocale, paliTextPath,
              translationLocale=None, translator=None):
  result = isValidPath(paliTextPath, translationLocale, translator)
  if result['isValid']:
    # this is a valid path
    if translationLocale:
      if reqPath.endswith('ContrastReading'):
        # contrast reading page
        result['htmlTitle'] = getHtmlTitle(urlLocale, result['texts'],
                                           translator, True)
        result['pageHtml'] = getContrastReadingPageHtml(translationLocale,
                               translator, result['node']['action'], reqPath)
      else:
        # translation page
        result['htmlTitle'] = getHtmlTitle(urlLocale, result['texts'],
                                           translator, False)
        result['pageHtml'] = getTranslationPageHtml(translationLocale,
                               translator, result['node']['action'], reqPath)
    else:
      # canon page
      result['htmlTitle'] = getHtmlTitle(urlLocale, result['texts'])
      result['pageHtml'] = getCanonPageHtml(result['node'], reqPath)

  return result


def getBodyDom(xmlUrl):
  # feed transformed data to minidom for processing
  dom = xml.dom.minidom.parseString(etree.tostring(paliXslt(xmlUrl)))
  # return only dom of body
  return dom.documentElement.getElementsByTagName('body')[0]


def getI18nLinks(xmlFilename, reqPath):
  template = getJinja2Env().get_template('i18nLinks.html')

  i18nLinksTemplateValues = getI18nLinksTemplateValues(xmlFilename)
  if i18nLinksTemplateValues:
    i18nLinksTemplateValues['reqPath'] = reqPath
    return template.render(i18nLinksTemplateValues);
  else:
    return u''


def getCanonPageHtml(node, reqPath):
  html = u''
  if 'action' in node:
    html += getI18nLinks(os.path.basename(node['action']), reqPath)
    # fetch xml
    xmlUrl = getCanonXmlUrl(node['action'])
    # return only innerHTML of body
    html += getBodyDom(xmlUrl).toxml()[6:-7]
  else:
    for child in node['child']:
      html += u'\n<a href="%s/%s">%s</a>\n' % (
                    reqPath, child['subpath'], child['text'])

  return html


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


def getAllLocalesTranslationsHtml(urlLocale):
  template = getJinja2Env().get_template('info.html')
  return template.render({'urlLocale': urlLocale,
                          'localeTranslations': getAllLocalesTranslationsTemplateValues()})


if __name__ == '__main__':
  # for test purpose
  pass
