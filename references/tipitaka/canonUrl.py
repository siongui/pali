#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, urllib, json
from lxml import etree
import xml.dom.minidom

xsl = open(os.path.join(os.path.dirname(__file__), 'static/symromn/cscd/tipitaka-latn.xsl')).read()
xslt_root = etree.fromstring(xsl)
transform = etree.XSLT(xslt_root)

urlInfoTree = json.loads(open(os.path.join(os.path.dirname(__file__), 'static/jsonTreeviewToc.json')).read())

translationInfo = {
'zh_TW': {
  'canon': {
    's0502m.mul0.xml': ['2'],
    's0502m.mul1.xml': ['2'],
    's0502m.mul2.xml': ['2'],
    's0502m.mul3.xml': ['2'],
    's0502m.mul4.xml': ['2'],
    's0505m.mul0.xml': ['1']
  },
  'source': {
    '1': ['郭良鋆', 'http://blog.yam.com/benji/article/34665984'],
    '2': ['了參法師(葉均)', 'http://nt.med.ncku.edu.tw/biochem/lsn/Tipitaka/Sutta/Khuddaka/Dhammapada/Dhammapada.htm'],
    '3': ['蕭式球', 'http://www.chilin.edu.hk/edu/report_section.asp?section_id=5']
  }
},
'en_US': {
  'canon': {
    's0502m.mul0.xml': ['1'],
    's0502m.mul1.xml': ['1'],
    's0502m.mul2.xml': ['1'],
    's0502m.mul3.xml': ['1'],
    's0502m.mul4.xml': ['1']
  },
  'source': {
    '1': ['Ṭhānissaro Bhikkhu', 'http://www.accesstoinsight.org/tipitaka/translators.html#than', 'http://www.accesstoinsight.org/lib/authors/thanissaro/dhammapada.pdf']
  }
}
};


def checkTranslationUrl(path, xmlFilename, url):
  for locale in translationInfo:
    localeUrl = url + '/' + locale

    if xmlFilename in translationInfo[locale]['canon']:
      sources = translationInfo[locale]['canon'][xmlFilename]
      for source in sources:
        translator = translationInfo[locale]['source'][source][0].decode('utf-8')

        if path == localeUrl:
          return True

        trUrl = localeUrl + '/' + translator
        if path == trUrl:
          return True

        crUrl = trUrl + '/' + 'ContrastReading'
        if path == crUrl:
          return True

  return False

def matchUrl(path, infoTree):
  if type(infoTree) is list:
    for subInfoTree in infoTree:
      if matchUrl(path, subInfoTree):
        return True
    return False

  if 'url' in infoTree.keys():
    url = infoTree['url']
    if path == url:
      return True

    if path.startswith(url):
      if 'child' in infoTree.keys():
        return matchUrl(path, infoTree['child'])

      if 'action' in infoTree.keys():
        # at the leaf of infoTree
        # path > url && path contains url, check if this is legal translation url
        return checkTranslationUrl(path, infoTree['action'], url)

      return False
    else:
      return False

  raise Exception('In matchUrl: should not be here')


def isValidCanonUrl(path):
  path = urllib.unquote(path).decode('utf-8')
  if path == '/canon':
    return True

  return matchUrl(path, urlInfoTree)


def getTranslationTitleInfo(path, xmlFilename, url):
  # FIXME: return translation title info instead of ''
  return ''


def recursiveGetTitle(path, infoTree):
  if type(infoTree) is list:
    title = ''
    for subInfoTree in infoTree:
      title += recursiveGetTitle(path, subInfoTree)
    return title

  if 'url' in infoTree.keys():
    url = infoTree['url']

    if url == path:
      return infoTree['text']

    if path.startswith(url):
      if 'child' in infoTree.keys():
        return recursiveGetTitle(path, infoTree['child']) + ' - ' + infoTree['text']

      if 'action' in infoTree.keys():
        # at the leaf of infoTree
        # path > url && path contains url, check if this is legal translation url
        return getTranslationTitleInfo(path, infoTree['action'], url) + infoTree['text']

      return ''
    else:
      return ''

  raise Exception('In recursiveGetTitle: should not be here')


def getTitleInfo(path):
  path = urllib.unquote(path).decode('utf-8')
  if path == '/canon':
    return 'Browse '

  return recursiveGetTitle(path, urlInfoTree) + ' - '


def getlocaleUrlInnerHTML(xmlFilename, locale, url):
  html = '<a href="%s">&lt;&lt; Original Pāḷi Text</a><br /><br />'.decode('utf-8') % url

  localeUrl = url + '/' + locale
  if xmlFilename in translationInfo[locale]['canon']:
    sources = translationInfo[locale]['canon'][xmlFilename]
    for source in sources:
      translator = translationInfo[locale]['source'][source][0].decode('utf-8')

      trUrl = localeUrl + '/' + translator
      crUrl = trUrl + '/' + 'ContrastReading'

      html += '<a href="%s" name="%s">%s</a>&nbsp;' % (trUrl, xmlFilename, translator) + \
              '(<a href="%s" name="%s">Contrast Reading</a>)<br />' % (crUrl, xmlFilename)
  else:
    raise Exception('In getlocaleUrlInnerHTML: no such xmlFilename')

  return html

def gettrUrlInnerHTML(xmlFilename, locale, source, url):
  xmlPath = os.path.join(os.path.dirname(__file__), 'static/symtranslation/' + locale + '/' + source + '/' + xmlFilename)

  html = '<a href="%s">&lt;&lt; Original Pāḷi Text</a>'.decode('utf-8') % url
  # read xml
  root = etree.fromstring(open(xmlPath).read())
  # transform xml with xslt
  root = transform(root)
  # feed transformed data to minidom for processing
  dom = xml.dom.minidom.parseString(etree.tostring(root))
  # return only innerHTML of body
  html += dom.documentElement.getElementsByTagName('body')[0].toxml()[6:-7]

  return html

def generateContrastReadingTable(oriBody, trBody):
  if (len(oriBody.childNodes) != len(trBody.childNodes)):
    raise Exception('two XML document body childs # not match')

  impl = xml.dom.minidom.getDOMImplementation()
  dom = impl.createDocument(None, 'table', None)
  tb = dom.documentElement
  tb.setAttribute('id', "contrastReadingTable")
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

def getContrastReadingUrlInnerHTML(xmlFilename, locale, source, url):
  html = '<a href="%s">&lt;&lt; Original Pāḷi Text</a><br /><br />'.decode('utf-8') % url

  oriXmlPath = os.path.join(os.path.dirname(__file__), 'static/symromn/cscd/' + xmlFilename)
  trXmlPath = os.path.join(os.path.dirname(__file__), 'static/symtranslation/' + locale + '/' + source + '/' + xmlFilename)

  # read xml
  oriRoot = etree.fromstring(open(oriXmlPath).read())
  # transform xml with xslt
  oriRoot = transform(oriRoot)
  # feed transformed data to minidom for processing
  oriDom = xml.dom.minidom.parseString(etree.tostring(oriRoot))
  oriBody = oriDom.documentElement.getElementsByTagName('body')[0]

  # read xml
  trRoot = etree.fromstring(open(trXmlPath).read())
  # transform xml with xslt
  trRoot = transform(trRoot)
  # feed transformed data to minidom for processing
  trDom = xml.dom.minidom.parseString(etree.tostring(trRoot))
  trBody = trDom.documentElement.getElementsByTagName('body')[0]

  html += generateContrastReadingTable(oriBody, trBody)

  return html

def getTranslationInnerHTML(path, xmlFilename, url):
  for locale in translationInfo:
    localeUrl = url + '/' + locale

    if path == localeUrl:
      return getlocaleUrlInnerHTML(xmlFilename, locale, url)

    if xmlFilename in translationInfo[locale]['canon']:
      sources = translationInfo[locale]['canon'][xmlFilename]
      for source in sources:
        translator = translationInfo[locale]['source'][source][0].decode('utf-8')

        trUrl = localeUrl + '/' + translator
        if path == trUrl:
          return gettrUrlInnerHTML(xmlFilename, locale, source, url)

        crUrl = trUrl + '/' + 'ContrastReading'
        if path == crUrl:
          return getContrastReadingUrlInnerHTML(xmlFilename, locale, source, url)

  return ''

def getTranslationHtml(xmlFilename, url):
  html = ''
  for locale in translationInfo:
    htmlLocale = ''
    localeUrl = url + '/' + locale

    if xmlFilename in translationInfo[locale]['canon']:
      htmlSources = ''

      sources = translationInfo[locale]['canon'][xmlFilename]
      for source in sources:
        translator = translationInfo[locale]['source'][source][0].decode('utf-8')

        trUrl = localeUrl + '/' + translator
        crUrl = trUrl + '/' + 'ContrastReading'

        htmlSources += '<a href="%s" name="%s">%s</a>&nbsp;' % (trUrl, xmlFilename, translator) + \
                       '(<a href="%s" name="%s">Contrast Reading</a>)<br />' % (crUrl, xmlFilename)

      if htmlSources != '':
        htmlLocale = '<a href="%s">%s</a>:<div style="padding-left: 1em;">%s</div>' % (localeUrl, locale, htmlSources)

    if htmlLocale != '':
      html += htmlLocale

  return html

def xml2Html(xmlFilename, url):
  html = ''
  # check whether there are translations
  htmlTranslation = getTranslationHtml(xmlFilename, url)
  if htmlTranslation != '':
    html += '<div id="showTranslation"><span>&#9658;</span><span>See Translation</span></div>'
    html += '<div id="htmlTranslation">%s</div>' % htmlTranslation

  # read xml
  root = etree.fromstring(open(os.path.join(os.path.dirname(__file__), 'static/symromn/cscd/' + xmlFilename)).read())
  # transform xml with xslt
  root = transform(root)
  # feed transformed data to minidom for processing
  dom = xml.dom.minidom.parseString(etree.tostring(root))
  html += '<div id="palitexts">'
  # return only innerHTML of body
  html += dom.documentElement.getElementsByTagName('body')[0].toxml()[6:-7]
  html += '</div>'

  return html

def getInnerHTML(path, infoTree):
  if type(infoTree) is list:
    html = ''
    for subInfoTree in infoTree:
      html += getInnerHTML(path, subInfoTree)
    return html

  if 'url' in infoTree.keys():
    url = infoTree['url']

    if url == path:
      if 'action' in infoTree.keys():
        return xml2Html(infoTree['action'], url)
      else:
        return getInnerHTML(path, infoTree['child'])

    if url.startswith(path):
      return '<a href="%s">' % url + infoTree['text'] + '</a><br />'

    if path.startswith(url):
      try:
        return getInnerHTML(path, infoTree['child'])
      except KeyError:
        # at the leaf of infoTree
        # path > url && path contains url, this is legal translation url
        return getTranslationInnerHTML(path, infoTree['action'], url)

    return ''

  raise Exception('In getInnerHTML: should not be here')


def getMainViewInnerHTML(path):
  path = urllib.unquote(path).decode('utf-8')

  container = '<div style="padding: 1em; background-color: #F0F8FF; min-height: 100%">'
  container += getInnerHTML(path, urlInfoTree)
  container += '</div>'

  return container
