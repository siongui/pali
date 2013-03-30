#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json, urllib2, re
from lxml import etree
import xml.dom.minidom

paliXmlUrlPrefix = u'http://epalitipitaka.appspot.com/romn/'
trXmlUrlPrefix = u'http://epalitipitaka.appspot.com/translation/'


with open(os.path.join(os.path.dirname(__file__), 'json/treeviewAll.json'), 'r') as f:
  treeviewData = json.loads(f.read())

result = urllib2.urlopen(os.path.join(paliXmlUrlPrefix, 'cscd/tipitaka-latn.xsl'))
xslt_root = etree.fromstring(result.read())
transform = etree.XSLT(xslt_root)

with open(os.path.join(os.path.dirname(__file__), 'json/translationInfo.json'), 'r') as f:
  translationInfo = json.loads(f.read())

with open(os.path.join(os.path.dirname(__file__), 'json/canonTextTranslation.json'), 'r') as f:
  canonTextTranslation = json.loads(f.read())


def nodeTextStrip(text):
  string = text

  # remove leading un-needed characters
  match = re.search(r'^[\d\s()-\.]+', string)
  if match:
    string = string[len(match.group()):]

  # remove trailing un-needed characters
  match = re.search(r'-\d$', string)
  if match:
    string = string[:-len(match.group())]

  return string


def nodeTextStrip2(text):
  string = nodeTextStrip(text)

  if string.endswith(u'pāḷi'):
    string = string[:-4]

  if string.endswith(u'nikāya'):
    string = string[:-6]

  if string.endswith(u'piṭaka'):
    string = string[:-6]

  return string


def translateNodeText(text, locale):
  string = nodeTextStrip(text)

  if locale in canonTextTranslation:
    if string in canonTextTranslation[locale]:
      return canonTextTranslation[locale][string]

  return text


def getHtmlTitle(urlLocale, texts, translator=None, contrastReading=None, i18n=None):
  #import logging
  #logging.getLogger().setLevel(logging.DEBUG)
  #logging.debug(texts)
  title = u''

  if texts:
    for text in reversed(texts):
      if urlLocale:
        trText = translateNodeText(text, urlLocale)
        if trText == text:
          title += nodeTextStrip2(text) + u' - '
        else:
          title += trText + u' - '
      else:
        title += nodeTextStrip2(text) + u' - '

  if translator:
    title = translator.decode('utf-8') + u' ' + i18n.gettext(u'Translation')  + u' - ' + title
  #i18n.gettext(u'Contrast Reading')

  return title


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

# @see http://stackoverflow.com/questions/1132941/least-astonishment-in-python-the-mutable-default-argument
def recursivelyCheck(node, path, texts):
  if path[0] is None:
    # check if all items are None
    for subPath in path:
      if subPath is not None:
        return {'isValid': False }
    # all items are None => True
    texts.append(node['text'])
    return {'isValid': True, 'node': node, 'texts': texts }

  else:
    for child in node['child']:
      if path[0].decode('utf-8') == child['subpath']:
        if 'action' in child:
          # check if all remaining items are None
          for subPath in path[1:]:
            if subPath is not None:
              return {'isValid': False }
          # all remaining items are None => True
          texts.append(node['text'])
          texts.append(child['text'])
          return {'isValid': True, 'node': child, 'texts': texts }
        else:
          texts.append(node['text'])
          return recursivelyCheck(child, path[1:], texts)

    return {'isValid': False }


def isValidCanonPath(path1, path2, path3, path4, path5):
  # rootNode is tipitaka, no commentaris and sub-commentaries
  rootNode = treeviewData['child'][0]
  path = [path1, path2, path3, path4, path5]

  return recursivelyCheck(rootNode, path, [])


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


def isValidTranslationOrContrastReadingPage(path1, path2, path3, path4, path5, locale, translator):
  # rootNode is tipitaka, no commentaris and sub-commentaries
  rootNode = treeviewData['child'][0]
  path = [path1, path2, path3, path4, path5]

  result = recursivelyCheck(rootNode, path, [])
  if result['isValid']:
    if 'action' in result['node']:
      if locale in translationInfo:
        xmlFilename = os.path.basename(result['node']['action'])
        if xmlFilename in translationInfo[locale]['canon']:
          for translatorCode in translationInfo[locale]['canon'][xmlFilename]:
            if translationInfo[locale]['source'][translatorCode][0] == translator.decode('utf-8'):
              return {'isValid': True, 'node': result['node'], 'texts': result['texts'] }

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
