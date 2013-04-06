#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, re, xml.dom.minidom

#errorXMLInfo = [['zh_TW', '3', 's0101m.mul1.xml'],
#                ['zh_TW', '3', 's0102m.mul2.xml'],
#                ['zh_TW', '3', 's0102m.mul8.xml'],
#                ['zh_TW', '3', 's0103m.mul7.xml'],
#                ['zh_TW', '3', 's0402m2.mul6.xml']]
errorXMLInfo = []

def replacement(match):
  pElmString = match.group()
  dom = xml.dom.minidom.parseString(pElmString.encode('utf-8'))
  pElm = dom.documentElement
  #print(pElm.toxml())
  return pElm.toxml()


def subXML(f):
  content = f.read().decode('UTF-16BE')
  re.sub(r'<p\srend=.+>.+</p>', replacement, content)
  return content


def convertXMLEncoding(path):
  print('processing ' + path + ' ...')
  with open(path, 'r') as f:
    content = subXML(f)

  with open(os.path.basename(path), 'w') as f:
    f.write(content.encode('utf-8'))


if __name__ == '__main__':
  for xmlInfo in errorXMLInfo:
    path = os.path.join('../translation', '%s/%s/%s' % (xmlInfo[0], xmlInfo[1], xmlInfo[2]))
    if not os.path.isfile(path):
      print('not file: %s' % path)
      exit(1)

    convertXMLEncoding(path)

