#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from lxml import etree
import xml.dom.minidom
from translationInfo import getTranslatorSource, getI18nLinksTemplateValues, getAllLocalesTranslationsTemplateValues
from template import getJinja2Env, getTranslationPageOriPaliLinkHtml, getContrastReadingPageOriPaliLinkHtml

paliXmlUrlPrefix = os.path.join(os.path.dirname(__file__), 'romn')
trXmlUrlPrefix = os.path.join(os.path.dirname(__file__), 'translation')

with open(os.path.join(paliXmlUrlPrefix, 'cscd/tipitaka-latn.xsl'), 'r') as f:
  xslt_root = etree.fromstring(f.read())
transform = etree.XSLT(xslt_root)


def getBodyDom(xmlUrl):
  # read xml
  with open(xmlUrl, 'r') as f:
    root = etree.fromstring(f.read())
  # transform xml with xslt
  root = transform(root)
  # feed transformed data to minidom for processing
  dom = xml.dom.minidom.parseString(etree.tostring(root))
  # return only dom of body
  return dom.documentElement.getElementsByTagName('body')[0]


def getI18nLinks(node, reqPath):
  xmlFilename = os.path.basename(node['action'])
  template = getJinja2Env().get_template('i18nLinks.html')

  i18nLinksTemplateValues = getI18nLinksTemplateValues(xmlFilename)
  if i18nLinksTemplateValues:
    i18nLinksTemplateValues['reqPath'] = reqPath
    return template.render(i18nLinksTemplateValues);
  else:
    return u''


def getCanonPageHtml(node, reqPath):
  # before using this funtion, make sure to call 'isValidCanonPath' first
  html = u''
  if 'action' in node:
    html += getI18nLinks(node, reqPath)
    # fetch xml
    xmlUrl = os.path.join(paliXmlUrlPrefix, node['action'])
    # return only innerHTML of body
    html += getBodyDom(xmlUrl).toxml()[6:-7]
  else:
    for child in node['child']:
      html += u'<a href="%s/%s">%s</a>' % (reqPath, child['subpath'], child['text'])

  return html


def getTranslationXmlBodyDom(locale, translator, node):
  # fetch xml
  xmlFilename = os.path.basename(node['action'])
  code = getTranslatorSource(xmlFilename, locale, translator)

  xmlUrl = os.path.join(trXmlUrlPrefix, '%s/%s/%s' % (locale, code, xmlFilename))
  return getBodyDom(xmlUrl)


def getTranslationPageHtml(locale, translator, node, reqPath):
  if 'action' not in node:
    raise Exception('In getTranslationPageHtml: action attribute not in node!')

  html = getTranslationPageOriPaliLinkHtml(reqPath)
  # return only innerHTML of body
  html += getTranslationXmlBodyDom(locale, translator, node).toxml()[6:-7]
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


def getContrastReadingPageHtml(locale, translator, node, reqPath):
  if 'action' not in node:
    raise Exception('In getTranslationPageHtml: action attribute not in node!')

  html = getContrastReadingPageOriPaliLinkHtml(reqPath)

  xmlUrl = os.path.join(paliXmlUrlPrefix, node['action'])
  oriBody= getBodyDom(xmlUrl)
  trBody = getTranslationXmlBodyDom(locale, translator, node)
  html += generateContrastReadingTable(oriBody, trBody)

  return html


def getAllLocalesTranslationsHtml(urlLocale):
  template = getJinja2Env().get_template('info.html')
  return template.render({'urlLocale': urlLocale,
                          'localeTranslations': getAllLocalesTranslationsTemplateValues()})


if __name__ == '__main__':
  # for test purpose
  pass
