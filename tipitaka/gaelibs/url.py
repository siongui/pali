#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json, urllib2, jinja2
from lxml import etree
import xml.dom.minidom

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../common/gae/libs'))
from misc import isProductionServer
if isProductionServer():
  paliXmlUrlPrefix = u'http://epalitipitaka.appspot.com/romn/'
  trXmlUrlPrefix = u'http://epalitipitaka.appspot.com/translation/'
else:
  paliXmlUrlPrefix = u'http://localhost:8080/romn/'
  trXmlUrlPrefix = u'http://localhost:8080/translation/'

with open(os.path.join(os.path.dirname(__file__), 'json/treeviewAll.json'), 'r') as f:
  treeviewData = json.loads(f.read())

result = urllib2.urlopen(os.path.join(paliXmlUrlPrefix, 'cscd/tipitaka-latn.xsl'))
xslt_root = etree.fromstring(result.read())
transform = etree.XSLT(xslt_root)

with open(os.path.join(os.path.dirname(__file__), 'json/translationInfo.json'), 'r') as f:
  translationInfo = json.loads(f.read())

jj2env = jinja2.Environment(
  loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

xmlFilename2PathInfo = {}


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
  linksHtml = u''
  xmlFilename = os.path.basename(node['action'])
  for locale in translationInfo:
    if xmlFilename in translationInfo[locale]['canon']:
      # FIXME: translate locale here
      linksHtml += u'<a href="javascript:void(0);">%s</a> :' % locale
      for translatorCode in translationInfo[locale]['canon'][xmlFilename]:
        translator = translationInfo[locale]['source'][translatorCode][0]
        linksHtml += (u'<div style="padding-left: 1em;">' +
                        u'<a href="%s/%s/%s">%s</a>' % (reqPath, locale, translator, translator) +
                        u' (<a href="%s/%s/%s/ContrastReading">%s</a>)' % (reqPath, locale, translator, i18n.gettext(u'Contrast Reading')) +
                      u'</div>')

  if linksHtml != u'':
    linksHtml = u'<div>%s <div>%s</div></div>' % (i18n.gettext(u'Translation of This Pāḷi Text'), linksHtml)

  return linksHtml


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
  if xmlFilename in translationInfo[locale]['canon']:
    for translatorCode in translationInfo[locale]['canon'][xmlFilename]:
      if translationInfo[locale]['source'][translatorCode][0] == translator.decode('utf-8'):
        code = translatorCode
        break
    try:
      code
    except:
      raise Exception('cannot find translatorCode')
  else:
    raise Exception("%s not in translationInfo[%s]['canon']" % (xmlFilename, locale))

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


def recursiveGetPath(node, pathPrefix, xmlFilename):
  path = pathPrefix + '/' + node['subpath']
  if 'action' in node:
    if os.path.basename(node['action']) == xmlFilename:
      return path
  else:
    for child in node['child']:
      result = recursiveGetPath(child, path, xmlFilename)
      if result:
        return result


def xmlFilename2Path(xmlFilename):
  if xmlFilename in xmlFilename2PathInfo:
    return xmlFilename2PathInfo[xmlFilename]
  result = recursiveGetPath(treeviewData['child'][0], u'', xmlFilename)
  if result:
    xmlFilename2PathInfo[xmlFilename] = result
  else:
    raise Exception('cannot get path of %s' % xmlFilename)
  return result


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
      for translatorCode in translationInfo[locale]['canon'][xmlFilename]:
        translation['translator'].append(translationInfo[locale]['source'][translatorCode][0])
      localeTranslation['translations'].append(translation)
    localeTranslations.append(localeTranslation)

  return template.render({'urlLocale': urlLocale, 'localeTranslations': localeTranslations});


if __name__ == '__main__':
  # for test purpose
  result = isValidCanonPath(None, None, None, None, None)
  if result['isValid'] is not True:
    print('test failure:')
    print('isValidCanonPath(None, None, None, None, None) is not True')

  result = isValidCanonPath(None, None, None, None, '123')
  if result['isValid'] is not False:
    print('test failure:')
    print("isValidCanonPath(None, None, None, None, '123') is not False")

  result = isValidCanonPath('sutta', 'dīgha', 'sīlakkhandhavagga', 'kūṭadantasuttaṃ', None)
  if result['isValid'] is not True:
    print('test failure:')
    print("isValidCanonPath('sutta', 'dīgha', 'sīlakkhandhavagga', 'kūṭadantasuttaṃ', None) is not True")

  result = isValidCanonPath('abhidhamma', 'kathāvatthu', 'puggalakathā', None, None)
  if result['isValid'] is not True:
    print('test failure:')
    print("isValidCanonPath('abhidhamma', 'kathāvatthu', 'puggalakathā', None, None) is not True")

  result = isValidCanonPath('sutta', 'dīgha', None, None, None)
  if result['isValid'] is not True:
    print('test failure:')
    print("isValidCanonPath('sutta', 'dīgha', None, None, None) is not True")

  result = isValidCanonPath('sutta', None, None, None, None)
  if result['isValid'] is not True:
    print('test failure:')
    print("isValidCanonPath('sutta', None, None, None, None) is not True")

  result = isValidCanonPath('sutta1', None, None, None, None)
  if result['isValid'] is not False:
    print('test failure:')
    print("isValidCanonPath('sutta', None, None, None, None) is not False")

  result = isValidCanonPath('abhidhamma', 'kathāvatthu2', 'puggalakathā', None, None)
  if result['isValid'] is not False:
    print('test failure:')
    print("isValidCanonPath('abhidhamma', 'kathāvatthu2', 'puggalakathā', None, None) is not False")

  result = isValidTranslationOrContrastReadingPage('sutta', 'khuddaka', 'dhammapada', 'pupphavaggo', None, 'zh_TW', '了參法師(葉均)')
  if result['isValid'] is not True:
    print('test failure:')
    print("isValidTranslationOrContrastReadingPage('sutta', 'khuddaka', 'dhammapada', 'pupphavaggo', None, 'zh_TW', '了參法師(葉均)') is not True")

  result = isValidTranslationOrContrastReadingPage('sutta', 'khuddaka', 'dhammapada', None, None, 'zh_TW', '了參法師(葉均)')
  if result['isValid'] is not False:
    print('test failure:')
    print("isValidTranslationOrContrastReadingPage('sutta', 'khuddaka', 'dhammapada', None, None, 'zh_TW', '了參法師(葉均)') is not False")

  result = isValidTranslationOrContrastReadingPage('sutta', 'khuddaka', 'dhammapada', 'pupphavaggo', None, 'zh_TW1', '了參法師(葉均)')
  if result['isValid'] is not False:
    print('test failure:')
    print("isValidTranslationOrContrastReadingPage('sutta', 'khuddaka', 'dhammapada', 'pupphavaggo', None, 'zh_TW1', '了參法師(葉均)') is not False")

  result = isValidTranslationOrContrastReadingPage('sutta', 'khuddaka', 'dhammapada', 'pupphavaggo', None, 'zh_TW', '1了參法師(葉均)')
  if result['isValid'] is not False:
    print('test failure:')
    print("isValidTranslationOrContrastReadingPage('sutta', 'khuddaka', 'dhammapada', 'pupphavaggo', None, 'zh_TW', '1了參法師(葉均)') is not False")
