#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, shutil
import xml.dom.minidom
import json
import re

def parseElement(element, url, indexDir, space=0):
  if len(element.childNodes) == 0:
    if element.nodeType == xml.dom.Node.TEXT_NODE:
      return
    if element.nodeType == xml.dom.Node.COMMENT_NODE:
      return
    if element.hasAttributes():
      print(" "*space + element.getAttribute('text'))
      print(" "*space + element.getAttribute('src'))
      if 'toc' in element.getAttribute('src'):
        getTocXml(url, indexDir, element.getAttribute('src') )
      return
  if len(element.childNodes) > 0:
    print(" "*space + element.getAttribute('text'))

    for childNode in element.childNodes:
      parseElement(childNode, url, indexDir, space + 2)

    return

  raise Exception('there should not be such node!')


def getTocXml(url, indexDir, src):
  if not os.path.exists(indexDir):
    os.makedirs(indexDir)
  os.system("wget %s%s -O %s%s" % (url, src, indexDir, os.path.basename(src) ) )

  dom = xml.dom.minidom.parse(indexDir + os.path.basename(src) )
  parseElement(dom.documentElement, url, indexDir)


def getTocs(indexDir):
  if os.path.exists(indexDir):
    # remove all dirs and sub-dirs
    shutil.rmtree(indexDir)

  getTocXml('http://www.tipitaka.org/romn/', indexDir, 'tipitaka_toc.xml')


def getPali(paliDir, src):
  url = 'http://www.tipitaka.org/romn/'
  if not os.path.exists(paliDir):
    os.makedirs(paliDir)

  os.system("wget %s%s -O %s%s" % (url, src, paliDir, os.path.basename(src) ) )


def parseToc(element, paliDir, indexDir, space=0):
  if len(element.childNodes) == 0:
    if element.nodeType == xml.dom.Node.TEXT_NODE:
      return
    if element.nodeType == xml.dom.Node.COMMENT_NODE:
      return
    if element.hasAttributes():
      print(" "*space + element.getAttribute('text'))
      #print(" "*space + element.getAttribute('src'))
      if 'toc' in element.getAttribute('src'):
        readToc(paliDir, indexDir, 
          os.path.basename(element.getAttribute('src')))
      else:
        getPali(paliDir, element.getAttribute('action'))
      return
  if len(element.childNodes) > 0:
    print(" "*space + element.getAttribute('text'))

    for childNode in element.childNodes:
      parseToc(childNode, paliDir, indexDir ,space + 2)

    return

  raise Exception('there should not be such node!')


def readToc(paliDir, indexDir, tocFilename):
  dom = xml.dom.minidom.parse(indexDir + tocFilename)
  parseToc(dom.documentElement, paliDir, indexDir)


def t2jProcessNodeAttr(element, space):
  dic = {}

  #info = ''
  for attr in element.attributes.keys():
    # four possible attributes: text, src, action, target
    if attr.upper() not in ['TEXT', 'SRC', 'ACTION', 'TARGET']:
      raise Exception('Impossible Attribute: ' + attr.upper())

    if attr.upper() != 'TARGET':
      if attr.upper() == 'ACTION':
        dic[attr] = os.path.basename(element.getAttribute(attr))
        if 'toc' in dic[attr]:
          raise Exception('"toc" in ACTION string')
      else:
        dic[attr] = element.getAttribute(attr)
    """
    info = info + ' ' * space + \
           attr.upper() + ': ' + \
           element.getAttribute(attr) + '\n'
    """

  if len(dic.keys()) == 0:
    return None

  #print(info)
  return dic


def t2jParseToc(element, tocDir, space=0, isRoot=True):
  if len(element.childNodes) == 0:
    if element.nodeType == xml.dom.Node.TEXT_NODE:
      return None

    if element.nodeType == xml.dom.Node.COMMENT_NODE:
      return None

    if element.nodeType == xml.dom.Node.ELEMENT_NODE:
      dic = t2jProcessNodeAttr(element, space)
      if 'src' in dic.keys():
        if 'toc' not in dic['src']:
          raise Exception('leaf node with SRC attribute, but has no "toc" in SRC string')
        if 'text' not in dic.keys():
          raise Exception('leaf node with SRC attribute, but has no TEXT attribute')
        dom = xml.dom.minidom.parse(tocDir + os.path.basename(element.getAttribute('src')))
        # FIXME: this assignment correct?
        del dic['src']
        dic['child'] = t2jParseToc(dom.documentElement, tocDir, space)
      else:
        if 'action' not in dic.keys():
          raise Exception('leaf node with no ACTION and SRC attribute!')
      if dic == None:
        raise Exception('leaf node returns no empty dic!')
      return dic

    raise Exception('there should not be such node!')
  else:
    if element.nodeType == xml.dom.Node.ELEMENT_NODE:
      dic = t2jProcessNodeAttr(element, space)
      if dic == None and not isRoot:
        raise Exception('not root node, not leaf node, and has no attribute')

      childList = []
      for childNode in element.childNodes:
        childDic = t2jParseToc(childNode, tocDir ,space + 2, False)
        if childDic != None:
          childList.append(childDic)

      if len(childList) == 0:
        raise Exception('childList length = 0')

      if dic == None:
        return childList
      else:
        dic['child'] = childList
        return dic

    raise Exception('there should not be such node!')


def tocFiles2JSVar():
  tocDir = os.path.join(os.path.dirname(__file__), '../static/romn/toc/')

  tocPath = tocDir + 'toc1.xml'
  dom = xml.dom.minidom.parse(tocPath)
  result = t2jParseToc(dom.documentElement, tocDir)
  print(json.dumps(result, sort_keys=True, indent=1))

  jsFilePath = os.path.join(os.path.dirname(__file__), '../static/js/') + 'jsonTreeviewToc.js'

  fd = open(jsFilePath, "w")
  fd.write('var jsonTreeviewToc = ')
  fd.write(json.dumps(result))
  fd.write(';')
  fd.close()


def getUrl(text, prefix):
  url = text

  p = re.compile('[\d\s()-\.]+')
  if p.match(url):
    url = url[len(p.match(url).group()):]

  p2 = re.compile('-\d$')
  if p2.search(url):
    url = url[:-len(p.search(url).group())]

  url = url.lower()

  if url.endswith(u'pāḷi'):
    url = url[:-4]

  if url.endswith(u'nikāya'):
    url = url[:-6]

  if url.endswith(u'piṭaka'):
    url = url[:-6]

  url = prefix + '/' + url

#  print(url)
  return url


def traverseTree(infoTree, prefix='/canon'):
  if type(infoTree) is list:
    for item in infoTree:
      traverseTree(item, prefix)
    return

  if 'text' in infoTree.keys():
    infoTree['url'] = getUrl(infoTree['text'], prefix)

    if 'child' in infoTree.keys():
      if 'action' in infoTree.keys():
        raise Exception('no such infoTree')
      traverseTree(infoTree['child'], infoTree['url'])
      return

    if 'action' in infoTree.keys():
      if 'child' in infoTree.keys():
        raise Exception('no such infoTree')
      return

  raise Exception('no such infoTree')


def tocFiles2Json():
  tocDir = os.path.join(os.path.dirname(__file__), '../static/romn/toc/')

  tocPath = tocDir + 'toc1.xml'
  dom = xml.dom.minidom.parse(tocPath)
  result = t2jParseToc(dom.documentElement, tocDir)
  traverseTree(result)
  print(json.dumps(result, sort_keys=True, indent=1))

  jsonFilePath = os.path.join(os.path.dirname(__file__), '../static/') + 'jsonTreeviewToc.json'

  fd = open(jsonFilePath, "w")
  fd.write(json.dumps(result, sort_keys=True, indent=1))
#  fd.write(json.dumps(result))
  fd.close()


if __name__ == '__main__':
  indexDir = os.path.join(os.path.dirname(__file__), 'index/')
  paliDir = os.path.join(os.path.dirname(__file__), 'pali/')
  #getTocs(indexDir)

  # get tipitaka
  #readToc(paliDir, indexDir, 'toc1.xml')

  # build JavaScrip variable from TOC files
  #tocFiles2JSVar()
  tocFiles2Json()
