#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys, shutil
import xml.dom.minidom
import json
import urllib


def decodeXML(xmlFiledata):
  dom = xml.dom.minidom.parseString(xmlFiledata)

  items = dom.getElementsByTagName("item")
  result = []
  for item in items:
    dictstr, wordstr, explainstr = decodeItem(item)
    result.append((dictstr, wordstr, explainstr))

  # return valus is "list of 3-tuples"
  return result


def decodeItem(item):
  dict = item.getElementsByTagName("dict")[0]
  word = item.getElementsByTagName("word")[0]
  explain = item.getElementsByTagName("explain")[0]

  dictstr = dict.childNodes[0].data
  wordstr = word.childNodes[0].data
  explainstr = HexStringToString(explain.childNodes[0].data)

  return dictstr, wordstr, explainstr


def HexStringToString(hexString):
  # convert hex string to utf8 string
  # example: "%2c%e3%80" -> "\x2C\xE3\x80"
  bytes = []
  hexStr = ''.join( hexString.split("%") )
  for i in range(0, len(hexStr), 2):
    bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

  # decode as utf8
  try:
    string = ''.join( bytes ).decode("utf-8")
  except UnicodeDecodeError:
    return hexString

  return string


if __name__ == '__main__':
  srcXmlDir = os.path.join(os.path.dirname(__file__), 'pali-dict-software-web1version/xml/')
  srcJsonFile1 = os.path.join(os.path.dirname(__file__), '../gae/libs/json/dicPrefixWordLists.json')
  srcJsonFile2 = os.path.join(os.path.dirname(__file__), '../gae/libs/json/dicPrefixGroup.json')
  dstAppEngDir = os.path.join(os.path.dirname(__file__), 'app-engine-json/')

  if not os.path.exists(srcXmlDir):
    print(srcXmlDir + ' does not exist!')
    sys.exit(1)

  if not os.path.exists(srcJsonFile1):
    print(srcJsonFile1 + ' does not exist!')
    sys.exit(1)

  if not os.path.exists(srcJsonFile2):
    print(srcJsonFile2 + ' does not exist!')
    sys.exit(1)

  # If old deployment folders exist, delete them.
  if os.path.exists(dstAppEngDir):
    # remove all dirs and sub-dirs
    shutil.rmtree(dstAppEngDir)

  with open(srcJsonFile1, 'r') as f:
    dicPrefixWordLists = json.loads(f.read())

  with open(srcJsonFile2, 'r') as f:
    dicPrefixGroup = json.loads(f.read())

  for firstCharOfWord in dicPrefixGroup:
    groupNum = dicPrefixGroup[firstCharOfWord]
    dstSubDir = os.path.join(dstAppEngDir, urllib.quote('jsons%d/json/%s' % (groupNum, firstCharOfWord.encode('utf-8'))).replace('%', 'Z') )

    if not os.path.exists(dstSubDir):
      os.makedirs(dstSubDir)

    # for all words start with the same first char
    for word in dicPrefixWordLists[firstCharOfWord]:
      srcFilePath = os.path.join( os.path.join( srcXmlDir, firstCharOfWord ), word + u'.xml')
      dstFilePath = os.path.join( dstSubDir, urllib.quote(word.encode('utf-8') + '.json').replace('%', 'Z') )

      # covert xml to json, andi then save them.
      with open(srcFilePath, 'r') as fsrc:
        with open(dstFilePath, 'w') as fdst:
          fdst.write(json.dumps(decodeXML(fsrc.read())))

    # generate app.yaml for each version
    dstAppYamlPath = os.path.join(dstAppEngDir, u'jsons%d/app.yaml' % groupNum)
    # if app.yaml already exists, continue forloop
    if os.path.exists(dstAppYamlPath):
      continue

    with open(dstAppYamlPath, 'w') as f:
      f.write(u'application: palidictionary\n')
      f.write(u'version: jsons%d\n' % groupNum)
      f.write(u'runtime: python27\n')
      f.write(u'api_version: 1\n')
      f.write(u'threadsafe: true\n')
      f.write(u'\n')
      f.write(u'handlers:\n')
      f.write(u'- url: /json\n')
      f.write(u'  static_dir: json\n')
      f.write(u'  mime_type: application/json\n')
      f.write(u'  http_headers:\n')
      f.write(u'    Access-Control-Allow-Origin: "*"\n')
