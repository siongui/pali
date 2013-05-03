#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json, urllib2, jinja2
from lxml import etree
import xml.dom.minidom
from pathInfo import xmlFilename2Path
from translationInfo import getTranslatorSource, getI18nLinksTemplateValues

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../common/gae/libs'))
from misc import isProductionServer
if isProductionServer():
  paliXmlUrlPrefix = u'http://epalitipitaka.appspot.com/romn/'
  trXmlUrlPrefix = u'http://epalitipitaka.appspot.com/translation/'
else:
  paliXmlUrlPrefix = u'http://localhost:8080/romn/'
  trXmlUrlPrefix = u'http://localhost:8080/translation/'

result = urllib2.urlopen(os.path.join(paliXmlUrlPrefix, 'cscd/tipitaka-latn.xsl'))
xslt_root = etree.fromstring(result.read())
transform = etree.XSLT(xslt_root)

with open(os.path.join(os.path.dirname(__file__), 'json/translationInfo.json'), 'r') as f:
  translationInfo = json.loads(f.read())

jj2env = jinja2.Environment(
  loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.i18n'])


def getBodyDom(xmlUrl):
  result = urllib2.urlopen(xmlUrl)
  # successfully fetch xml
  root = etree.fromstring(result.read())
  # transform xml with xslt
  root = transform(root)
  # feed transformed data to minidom for processing
  dom = xml.dom.minidom.parseString(etree.tostring(root))
  # return only dom of body
  return dom.documentElement.getElementsByTagName('body')[0]


def getI18nLinks(node, reqPath, i18n):
  xmlFilename = os.path.basename(node['action'])
  template = jj2env.get_template('i18nLinks.html')

  i18nLinksTemplateValues = getI18nLinksTemplateValues(xmlFilename)
  if i18nLinksTemplateValues:
    # FIXME: remove i18n argument and from webapp2 import i18n in global scope
    jj2env.install_gettext_translations(i18n)
    i18nLinksTemplateValues['reqPath'] = reqPath
    return template.render(i18nLinksTemplateValues);
  else:
    return u''


def getCanonPageHtml(node, reqPath, i18n):
  # before using this funtion, make sure to call 'isValidCanonPath' first
  html = u''
  if 'action' in node:
    html += getI18nLinks(node, reqPath, i18n)
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


def getTranslationPageHtml(locale, translator, node, reqPath, i18n):
  if 'action' not in node:
    raise Exception('In getTranslationPageHtml: action attribute not in node!')

  html = u'<div>&lt;&lt; <a href="%s">%s</a></div>' % (os.path.sep.join(reqPath.split(os.path.sep)[:-2]), i18n.gettext(u'Original Pāḷi Text'))
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


def getContrastReadingPageHtml(locale, translator, node, reqPath, i18n):
  if 'action' not in node:
    raise Exception('In getTranslationPageHtml: action attribute not in node!')

  html = u'<div>&lt;&lt; <a href="%s">%s</a></div>' % (os.path.sep.join(reqPath.split(os.path.sep)[:-3]), i18n.gettext(u'Original Pāḷi Text'))

  xmlUrl = os.path.join(paliXmlUrlPrefix, node['action'])
  oriBody= getBodyDom(xmlUrl)
  trBody = getTranslationXmlBodyDom(locale, translator, node)
  html += generateContrastReadingTable(oriBody, trBody)

  return html


def getAllLocalesTranslationsHtml(urlLocale):
  template = jj2env.get_template('info.html')
  localeTranslations = []
  for locale in translationInfo:
    localeTranslation = { 'locale': locale }
    localeTranslation['translations'] = []
    for xmlFilename in translationInfo[locale]['canon']:
      translation = { 'path': xmlFilename2Path(xmlFilename),
                      'xmlFilename': xmlFilename }
      translation['translator'] = []
      for localeXmlTranslation in translationInfo[locale]['canon'][xmlFilename]:
        translation['translator'].append(translationInfo[locale]['source'][ localeXmlTranslation['source'] ][0])
      localeTranslation['translations'].append(translation)
    localeTranslations.append(localeTranslation)

  return template.render({'urlLocale': urlLocale, 'localeTranslations': localeTranslations});


if __name__ == '__main__':
  # for test purpose
  pass
