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
                                           translator, result['node'], reqPath)
      else:
        # translation page
        result['htmlTitle'] = getHtmlTitle(urlLocale, result['texts'],
                                           translator, False)
        result['pageHtml'] = getTranslationPageHtml(translationLocale,
                                           translator, result['node'], reqPath)
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


def getTranslationXmlBodyDom(translationLocale, translator, node):
  return getBodyDom(getTranslationXmlUrl(os.path.basename(node['action']),
                                         translationLocale, translator))


def getTranslationPageHtml(translationLocale, translator, node, reqPath):
  if 'action' not in node:
    raise Exception('In getTranslationPageHtml: action attribute not in node!')

  html = getTranslationPageOriPaliLinkHtml(reqPath)
  # return only innerHTML of body
  html += getTranslationXmlBodyDom(translationLocale, translator, node).toxml()[6:-7]
  return html


def generateContrastReadingTable(oriBody, trBody):
  if (len(oriBody.childNodes) != len(trBody.childNodes)):
    raise Exception('two XML document body childs # not match')

  impl = xml.dom.minidom.getDOMImplementation()
  dom = impl.createDocument(None, 'table', None)
  tb = dom.documentElement
  tb.setAttribute('style', "width: 100%")

  for i in range(len(oriBody.childNodes)):
    if oriBody.childNodes[i].nodeType != xml.dom.Node.ELEMENT_NODE and \
       trBody.childNodes[i].nodeType != xml.dom.Node.ELEMENT_NODE:
      continue

    td1 = dom.createElement('td');
    td1.appendChild(oriBody.childNodes[i].cloneNode(deep=True))
    td1.setAttribute('style', "width: 50%")

    td2 = dom.createElement('td');
    td2.appendChild(trBody.childNodes[i].cloneNode(deep=True))
    td2.setAttribute('style', "width: 50%")

    tr = dom.createElement('tr');
    tr.setAttribute('style', "text-align: left")
    tr.appendChild(td1)
    tr.appendChild(td2)

    tb.appendChild(tr)

  return tb.toxml()


def getContrastReadingPageHtml(translationLocale, translator, node, reqPath):
  if 'action' not in node:
    raise Exception('In getTranslationPageHtml: action attribute not in node!')

  html = getContrastReadingPageOriPaliLinkHtml(reqPath)

  xmlUrl = getCanonXmlUrl(node['action'])
  oriBody= getBodyDom(xmlUrl)
  trBody = getTranslationXmlBodyDom(translationLocale, translator, node)
  html += generateContrastReadingTable(oriBody, trBody)

  return html


def getAllLocalesTranslationsHtml(urlLocale):
  template = getJinja2Env().get_template('info.html')
  return template.render({'urlLocale': urlLocale,
                          'localeTranslations': getAllLocalesTranslationsTemplateValues()})


if __name__ == '__main__':
  # for test purpose
  pass
