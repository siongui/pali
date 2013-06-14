#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import shutil
import urllib2
import xml.dom.minidom

from variables import getRomnDir
from variables import getInfoFilePath

urlPrefix = 'http://www.tipitaka.org/romn/'
rootTocXmlSrc = 'tipitaka_toc.xml'
overwriteIfExist = False
"""
observation:
  1. All meaningful node has attribute 'text'
  2. node with 'action' attribute is leaf
"""
separator = u'#@%'
infoFileContent = ''


def getPaliXml(action, space):
  url = os.path.join(urlPrefix, action)
  path = os.path.join(getRomnDir(), action)

  if not os.path.exists(os.path.dirname(path)):
    os.makedirs(os.path.dirname(path))

  download(url, path, space)


def download(url, path, space):
  if os.path.isfile(path) and not overwriteIfExist:
    return
  print(' '*space + 'downloading [%s] ...' % url)
  response = urllib2.urlopen(url)
  with open(path, 'w') as f:
    f.write(response.read())
  print(' '*space + '[%s] saved!' % path)


def writeInfoFile(element, depth):
  if element.hasAttribute('action'):
    # leaf
    info = str(depth) + separator + element.getAttribute('text') + separator + element.getAttribute('action') + '\n'
  else:
    # not leaf
    info = str(depth) + separator + element.getAttribute('text') + '\n'
  global infoFileContent
  infoFileContent += info


def printAttrs(element, space):
  sys.stdout.write(' '*space)
  for attr in element.attributes.items():
    name = attr[0]
    value = attr[1]
    sys.stdout.write('[' + name + '] ' + value + '   ')
  sys.stdout.write('\n')
  writeInfoFile(element, space)


def parseTocElement(element, space):
  if len(element.childNodes) == 0:
    if element.nodeType == xml.dom.Node.TEXT_NODE:
      # meaningless leaf node
      return
    elif element.nodeType == xml.dom.Node.COMMENT_NODE:
      # meaningless leaf node
      return
    elif element.hasAttributes():
      printAttrs(element, space)
      if (element.hasAttribute('src')):
        getTocXml(element.getAttribute('src'), space)
      if (element.hasAttribute('action')):
        getPaliXml(element.getAttribute('action'), space)
    else:
      raise Exception('In parseTocElement: strange node');
  else:
    if element.hasAttributes():
      printAttrs(element, space)
    for childNode in element.childNodes:
      parseTocElement(childNode, space + 2)


def getTocXml(src, space=0):
  url = os.path.join(urlPrefix, src)
  path = os.path.join(getRomnDir(), src)

  if not os.path.exists(os.path.dirname(path)):
    os.makedirs(os.path.dirname(path))

  download(url, path, space)

  dom = xml.dom.minidom.parse(path)
  parseTocElement(dom.documentElement, space)


if __name__ == '__main__':
  getTocXml(rootTocXmlSrc)

  # add this fake node to force stack update in next script
  infoFileContent += (u'2' + separator + u'fake')

  if not os.path.exists(os.path.dirname(getInfoFilePath())):
    os.makedirs(os.path.dirname(getInfoFilePath()))
  with open(getInfoFilePath(), 'w') as f:
    f.write(infoFileContent.encode('utf-8'))

  getPaliXml('cscd/tipitaka-latn.xsl', 0)
  getPaliXml('cscd/tipitaka-latn.css', 0)
