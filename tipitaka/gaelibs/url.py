#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json
from google.appengine.api import urlfetch
from lxml import etree
import xml.dom.minidom

paliXmlUrlPrefix = u'http://epalitipitaka.appspot.com/romn/'
trXmlUrlPrefix = u'http://epalitipitaka.appspot.com/translation/'


with open(os.path.join(os.path.dirname(__file__), 'json/treeviewAll.json'), 'r') as f:
  treeviewData = json.loads(f.read())

result = urlfetch.fetch(os.path.join(paliXmlUrlPrefix, 'cscd/tipitaka-latn.xsl'))
if result.status_code == 200:
  xslt_root = etree.fromstring(result.content)
  transform = etree.XSLT(xslt_root)
else:
  raise Exception('cannot fetch xsl file!')

with open(os.path.join(os.path.dirname(__file__), 'json/translationInfo.json'), 'r') as f:
  translationInfo = json.loads(f.read())

with open(os.path.join(os.path.dirname(__file__), 'json/canonName.json'), 'r') as f:
  canonName = json.loads(f.read())


def getHtmlTitle(userLocale, reqHandlerName, i18n):
  return ''


def getBodyDom(xmlUrl):
  result = urlfetch.fetch(xmlUrl)
  if result.status_code == 200:
    # successfully fetch xml
    root = etree.fromstring(result.content)
    # transform xml with xslt
    root = transform(root)
    # feed transformed data to minidom for processing
    dom = xml.dom.minidom.parseString(etree.tostring(root))
    # return only dom of body
    return dom.documentElement.getElementsByTagName('body')[0]
  else:
    # fail to fetch xml
    raise Exception('cannot fetch %s' % xmlUrl)


def recursivelyCheck(node, path):
  if path[0] is None:
    # check if all items are None
    for subPath in path:
      if subPath is not None:
        return {'isValid': False }
    # all items are None => True
    return {'isValid': True, 'node': node }

  else:
    for child in node['child']:
      if path[0].decode('utf-8') == child['subpath']:
        if 'action' in child:
          # check if all remaining items are None
          for subPath in path[1:]:
            if subPath is not None:
              return {'isValid': False }
          # all remaining items are None => True
          return {'isValid': True, 'node': child }
        else:
          return recursivelyCheck(child, path[1:])

    return {'isValid': False }


def isValidCanonPath(path1, path2, path3, path4, path5):
  # rootNode is tipitaka, no commentaris and sub-commentaries
  rootNode = treeviewData['child'][0]
  path = [path1, path2, path3, path4, path5]

  return recursivelyCheck(rootNode, path)


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


def recursivelyCheck2(node, path):
  for child in node['child']:
    if path[0].decode('utf-8') == child['subpath']:
      if 'action' in child:
        # check if all remaining items are None
        for subPath in path[1:]:
          if subPath is not None:
            return {'isValid': False }
        # all remaining items are None => True
        return {'isValid': True, 'node': child }
      else:
        if len(path) == 1:
          return {'isValid': False }
        elif path[1] is None:
          return {'isValid': False }
        else:
          return recursivelyCheck2(child, path[1:])

  return {'isValid': False }


def isValidTranslationOrContrastReadingPage(path1, path2, path3, path4, path5, locale, translator):
  # rootNode is tipitaka, no commentaris and sub-commentaries
  rootNode = treeviewData['child'][0]
  path = [path1, path2, path3, path4, path5]

  result = recursivelyCheck2(rootNode, path)
  if result['isValid']:
    if locale in translationInfo:
      xmlFilename = os.path.basename(result['node']['action'])
      if xmlFilename in translationInfo[locale]['canon']:
        for translatorCode in translationInfo[locale]['canon'][xmlFilename]:
          if translationInfo[locale]['source'][translatorCode][0] == translator.decode('utf-8'):
            return {'isValid': True, 'node': result['node'] }
        return {'isValid': False }
      else:
        return {'isValid': False }
    else:
      return {'isValid': False }
  else:
    return {'isValid': False }


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


if __name__ == '__main__':
  # for test purpose
  if isValidCanonPath(None, None, None, None, None) is not True:
    print('test failure:')
    print('isValidCanonPath(None, None, None, None, None) is not True')

  if isValidCanonPath(None, None, None, None, '123') is not False:
    print('test failure:')
    print("isValidCanonPath(None, None, None, None, '123') is not False")

  if isValidCanonPath('sutta', 'dīgha', 'sīlakkhandhavagga', 'kūṭadantasuttaṃ', None) is not True:
    print('test failure:')
    print("isValidCanonPath('sutta', 'dīgha', 'sīlakkhandhavagga', 'kūṭadantasuttaṃ', None) is not True")

  if isValidCanonPath('abhidhamma', 'kathāvatthu', 'puggalakathā', None, None) is not True:
    print('test failure:')
    print("isValidCanonPath('abhidhamma', 'kathāvatthu', 'puggalakathā', None, None) is not True")

  if isValidCanonPath('sutta', 'dīgha', None, None, None) is not True:
    print('test failure:')
    print("isValidCanonPath('sutta', 'dīgha', None, None, None) is not True")

  if isValidCanonPath('sutta', None, None, None, None) is not True:
    print('test failure:')
    print("isValidCanonPath('sutta', None, None, None, None) is not True")

  if isValidCanonPath('sutta1', None, None, None, None) is not False:
    print('test failure:')
    print("isValidCanonPath('sutta', None, None, None, None) is not False")

  if isValidCanonPath('abhidhamma', 'kathāvatthu2', 'puggalakathā', None, None) is not False:
    print('test failure:')
    print("isValidCanonPath('abhidhamma', 'kathāvatthu2', 'puggalakathā', None, None) is not False")

  print(getCanonPageHtml(None, 'sutta', 'dīgha', None, None, None, u'/canon/sutta/dīgha'))
  print(getCanonPageHtml(None, 'sutta', 'dīgha', 'sīlakkhandhavagga', None, None, u'/canon/sutta/dīgha/sīlakkhandhavagga'))
  print(getCanonPageHtml(None, 'sutta', 'dīgha', 'sīlakkhandhavagga', 'kūṭadantasuttaṃ', None, u'/canon/sutta/dīgha/sīlakkhandhavagga/kūṭadantasuttaṃ'))
  print(getCanonPageHtml(None, 'abhidhamma', 'kathāvatthu', 'puggalakathā', None, None, u'/canon/abhidhamma/kathāvatthu/puggalakathā'))
