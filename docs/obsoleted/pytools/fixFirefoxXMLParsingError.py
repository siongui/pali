#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, re, xml.dom.minidom

#errorXMLInfo = [['zh_TW', '3', 's0101m.mul1.xml'],
#                ['zh_TW', '3', 's0102m.mul2.xml'],
#                ['zh_TW', '5', 's0102m.mul6.xml'],
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


def convertXMLEncoding2(path):
  print('processing ' + path + ' ...')
  os.system('iconv -f UTF-16BE -t UTF-8 %s' % path)

  with open(path, 'r') as f:
    newFileContent = re.sub(r'encoding="UTF-16"', r'encoding="UTF-8"', f.read())

  with open(path, 'w') as f:
    f.write(newFileContent)


if __name__ == '__main__':
  for xmlInfo in errorXMLInfo:
    path = os.path.join( os.path.join(os.path.dirname(__file__), '../translation'), '%s/%s/%s' % (xmlInfo[0], xmlInfo[1], xmlInfo[2]))
    if not os.path.isfile(path):
      print('not file: %s' % path)
      exit(1)

    #convertXMLEncoding(path)
    convertXMLEncoding2(path)

