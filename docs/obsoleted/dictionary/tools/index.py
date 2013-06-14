#!/usr/bin/env python
# -*- coding:utf-8 -*-

# build index of pali words into JavaScript Array variables

import os, sys
import shutil
import xml.dom.minidom
import json
import urllib

prefix_code = {
#  "°" : "uc",
#  "-" : "dash",
  "a" : "a",
  "ā" : "aa",
  "b" : "b",
  "c" : "c",
  "d" : "d",
  "ḍ" : "dotd",
  "e" : "e",
  "g" : "g",
  "h" : "h",
  "i" : "i",
  "ī" : "ii",
  "j" : "j",
  "k" : "k",
  "l" : "l",
  "ḷ" : "dotl",
  "m" : "m",
#  "ṃ" : "dotm",
  "n" : "n",
  "ñ" : "tilden",
#  "ṇ" : "dotn",
#  "ṅ" : "ndot",
#  "ŋ" : "ngng",
  "o" : "o",
  "p" : "p",
  "r" : "r",
  "s" : "s",
  "t" : "t",
  "ṭ" : "dott",
  "u" : "u",
  "ū" : "uu",
  "v" : "v",
  "y" : "y",
}


def usage():
  print("Usage:")
  print("$ python index.py index")
  print("$ python index.py group")
  print("$ python index.py stats")
  print("$ python index.py cpdir")
  print("$ python index.py js")


def buildJSONIndex(xmlDir, savedName):
  wordCount = {}
  wordCount['all'] = 0

  trueWordCount = {}
  trueWordCount['all'] = 0

  dicPrefixWordLists = {}

  # get words start with prefix 'key'
  for key in prefix_code.keys():
    # get all the files under folder name 'key'
    fileNames = os.listdir(xmlDir + key)

    wordCount[key] = 0
    trueWordCount[key] = 0
    dicPrefixWordLists[key] = []

    # iterate all words start with prefix 'key'
    for fileName in fileNames:
      wordCount['all'] += 1
      wordCount[key] += 1

      fileName = unicode(fileName.decode('utf8'))
      filaPath = xmlDir + key + '/' + fileName.encode('utf-8')
      fileData = open(filaPath.decode('utf-8'), 'r').read()

      # parse the xml data in the file
      dom = xml.dom.minidom.parseString(fileData)

      # iterate all the 'word' tag inside a xml file
      words = dom.getElementsByTagName('word')
      for word in words:
        wordStr = word.childNodes[0].data
        # FIXME: is lower() safe here?
        if (wordStr.lower() == fileName[:-4]):
          # This is a "true" word
          dicPrefixWordLists[key].append(fileName[:-4])
          trueWordCount['all'] += 1
          trueWordCount[key] += 1
          break

  # sort the words
  for key in dicPrefixWordLists.keys():
    dicPrefixWordLists[key].sort()

  # dicPrefixWordLists = {
  #   "a" : [ ... ]
  #   "ā" : [ ... ],
  #   "b" : [ ... ],
  #   "c" : [ ... ],
  #   ...
  # }
  # save the indexes in JSON-format to file
  fd = open(savedName, "w")
  fd.write(json.dumps(dicPrefixWordLists))
  fd.close()

  # print statistics
  for key in prefix_code.keys():
    print('word count %s: %d' % (key, wordCount[key]))
    print('true word count %s: %d' % (key, trueWordCount[key]))

  print('word count all: %d' % wordCount['all'])
  print('true word count all: %d' % trueWordCount['all'])


def stats(savedName, groupedSavedName):
  # dicPrefixWordLists = {
  #   "a" : [ ... ]
  #   "ā" : [ ... ],
  #   "b" : [ ... ],
  #   "c" : [ ... ],
  #   ...
  # }
  dicPrefixWordLists = json.loads(open(savedName).read())

  # print counts of words under each prefix
  allCount = 0
  for key in dicPrefixWordLists.keys():
    print('# of %s words: %d' %(key, len(dicPrefixWordLists[key])) )
    allCount += len(dicPrefixWordLists[key])
  print('all words count: %d' % allCount)

  raw_input('press Enter...')
  os.system('clear')

  # print words under each 'prefix' belongs to which version
  groupInfo = json.loads(open(groupedSavedName).read())
  for key in groupInfo['version'].keys():
    print('%s belongs to version #%d' % (key, groupInfo['version'][key]))

  raw_input('press Enter...')
  os.system('clear')

  showRecursiveVariable(groupInfo['dir'])


def buildWordsGroup(savedName, groupedSavedName, debug=False):
  # dicPrefixWordLists = {
  #   "a" : [ ... ]
  #   "ā" : [ ... ],
  #   "b" : [ ... ],
  #   "c" : [ ... ],
  #   ...
  # }
  dicPrefixWordLists = json.loads(open(savedName).read())

  groupInfo = {}

  # step 1:
  # GAE allows at most 10,000 files for each version
  versionLimitCount = 9900
  groupInfo['version'] = {}

  groupIndex = 0
  wordCount = 0
  for prefix in dicPrefixWordLists.keys():
    prefixWordCount = len(dicPrefixWordLists[prefix])

    if (prefixWordCount > versionLimitCount):
      raise Exception("%s too large: %d" % (prefix, prefixWordCount))

    if (prefixWordCount + wordCount < versionLimitCount):
      wordCount += prefixWordCount
      groupInfo['version'][prefix] = groupIndex
    else:
      wordCount = prefixWordCount
      groupIndex += 1
      groupInfo['version'][prefix] = groupIndex

  # step 2:
  # GAE allows at most 1,000 files for each directory
  dirCountLimit = 995

  for prefix in dicPrefixWordLists.keys():
    prefixWordCount = len(dicPrefixWordLists[prefix])
    if (prefixWordCount > dirCountLimit):
      if debug:
        print('%s # %d (too large)' %(prefix, prefixWordCount))
      tmpObj = groupByPrefixUnderCountLimit(dicPrefixWordLists[prefix], dirCountLimit, 2)
      del dicPrefixWordLists[prefix]
      dicPrefixWordLists[prefix] = tmpObj
    else:
      if debug:
        print('%s # %d' %(prefix, prefixWordCount))

  if debug:
    raw_input('press Enter...')
    os.system('clear')

    # show re-grouped dicPrefixWordLists
    showRecursiveVariable(dicPrefixWordLists)

  groupInfo['dir'] = dicPrefixWordLists

  # step 3:
  # save the grouped variable
  # example:
  # groupInfo = {
  #   'version' : {
  #       'a' : 0,
  #       'b' : 0,
  #       ...
  #     },
  #
  #   'dir': {
  #       'a' : {},
  #       'b' : [],
  #       ...
  #     }
  # }
  fd = open(groupedSavedName, "w")
  fd.write(json.dumps(groupInfo))
  fd.close()


def showRecursiveVariable(var, space=1):
  if type(var) is type([]):
    print(': %d' % len(var))
  elif type(var) is type({}):
    for key in var.keys():
      if type(var[key]) is type([]):
        sys.stdout.write('  '*space + '%s ' % key)
      else:
        print('  '*space + '%s + (over limit, break)' % key)
      showRecursiveVariable(var[key], space + 1)
  else:
    raise Exception('only [] or {} is allowed!')


def groupByPrefixUnderCountLimit(wordsArray, countLimit, digit, debug=False):
  group = {}

  # group by first 'digit'-letter
  for word in wordsArray:
    prefix = word[:digit]
    if prefix in group:
      group[prefix].append(word)
    else:
      group[prefix] = []
      group[prefix].append(word)

  # check if the length of array > countLimit
  for prefix in group:
    prefixWordCount = len(group[prefix])
    if (prefixWordCount > countLimit):
      # still > countLimit, recursively call self
      if debug:
        print('%s # %d (too large)' %(prefix, prefixWordCount))
      tmpObj = groupByPrefixUnderCountLimit(group[prefix], countLimit, digit + 1, debug)
      del group[prefix]
      group[prefix] = tmpObj
    else:
      if debug:
        print('%s # %d' %(prefix, prefixWordCount))

  if debug:
    raw_input('press Enter...')
    os.system('clear')

  return group


def buildJSONDeployDir(xmlDir, dpDirName, groupedSavedName):
  if os.path.exists(dpDirName):
    # remove all dirs and sub-dirs
    shutil.rmtree(dpDirName)

  # load pre-built indexes
  groupInfo = json.loads(open(groupedSavedName).read())

  versionInfo = groupInfo['version']

  # example:
  # versionInfo = {
  #   'a' : 0,
  #   'b' : 0,
  #   'c' : 1,
  #   'd' : 2
  # }
  # ==>
  # versions = {
  #   0 : ['a', 'b'],
  #   1 : ['c'],
  #   2 : ['d']
  # }
  versions = {}
  for prefix in versionInfo.keys():
    if versionInfo[prefix] in versions:
      versions[versionInfo[prefix]].append(prefix)
    else:
      versions[versionInfo[prefix]] = []
      versions[versionInfo[prefix]].append(prefix)

  for version in versions.keys():
    print('version %d:' % version)
    print(versions[version])

  dirInfo = groupInfo['dir']

  # iterate each version in all versions
  for version in versions:
    # destination directory of each version
    versionDir = dpDirName + 'version%d/' % version
    print(versionDir)

    # iterate all prefixes in each version
    for prefix in versions[version]:
      # source directory of words start with 'prefix'
      srcDir = xmlDir + prefix + '/'
      if not os.path.exists(srcDir):
        raise Exception('%s does not exist!' % srcDir)
      print(srcDir)

      count = iterateAllWordsInRecursiveVariable(dirInfo[prefix], prefix, versionDir, srcDir)
      print('%d' % count)

    # generate app.yaml for each version
    fd = open(versionDir + 'app.yaml', "w")
    fd.write('application: palidictionary\n')
    fd.write('version: json%d\n' % version)
    fd.write('runtime: python27\n')
    fd.write('api_version: 1\n')
    fd.write('threadsafe: true\n')
    fd.write('\n')
    fd.write('handlers:\n')
    fd.write('- url: /json\n')
    fd.write('  static_dir: json\n')
    fd.write('  mime_type: application/json\n')
    fd.write('  http_headers:\n')
    fd.write('    Access-Control-Allow-Origin: "*"\n')
    fd.close()


def iterateAllWordsInRecursiveVariable(var, prefix, versionDir, srcDir):
  wordCount = 0
  if type(var) is type([]):
    for word in var:
      srcFile = srcDir + word + '.xml'
      if not os.path.exists(srcFile):
        raise Exception('%s does not exist!' % srcFile)

      dstFile = versionDir + 'json/' + urllib.quote(prefix.encode('utf-8') + '/' + word.encode('utf-8') + '.json').replace('%', 'Z')

      if not os.path.exists(os.path.dirname(dstFile)):
        os.makedirs(os.path.dirname(dstFile))

      dstFd = open(dstFile, 'w')
      dstFd.write(json.dumps(xmlToJson(word, open(srcFile).read())))
      dstFd.close()

      wordCount += 1
  elif type(var) is type({}):
    for key in var.keys():
      wordCount += iterateAllWordsInRecursiveVariable(var[key], prefix + '/' + key, versionDir, srcDir)
  else:
    raise Exception('only [] or {} is allowed!')

  return wordCount


def xmlToJson(word, xmlFiledata):
  jsonData = {}
  jsonData['word'] = word
  jsonData['data'] = decodeXML(xmlFiledata)

  return jsonData


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
    string = u"Sorry! Something wrong with the database. We cannot get explain of this word in this dictionary."

  return string


def buildJS(savedName, groupedSavedName, jsName):
  # dicPrefixWordLists = {
  #   "a" : [ ... ]
  #   "ā" : [ ... ],
  #   "b" : [ ... ],
  #   "c" : [ ... ],
  #   ...
  # }
  dicPrefixWordLists = json.loads(open(savedName).read())
  # example:
  # groupInfo = {
  #   'version' : {
  #       'a' : 0,
  #       'b' : 0,
  #       ...
  #     },
  #
  #   'dir': {
  #       'a' : {},
  #       'b' : [],
  #       ...
  #     }
  # }
  groupInfo = json.loads(open(groupedSavedName).read())

  groupInfo['dir'] = stripWordsInRecursiveVariable(groupInfo['dir'])

  fd = open(jsName, "w")
  fd.write('var dicPrefixWordLists = ')
  fd.write(json.dumps(dicPrefixWordLists))
  fd.write(';\n')
  fd.write('var groupInfo = ')
  fd.write(json.dumps(groupInfo))
  fd.write(';\n')
  fd.close()


def stripWordsInRecursiveVariable(var):
  strippedVar = None
  if type(var) is type([]):
    strippedVar = []
  elif type(var) is type({}):
    strippedVar = {}
    for key in var.keys():
      strippedVar[key] = stripWordsInRecursiveVariable(var[key])
  else:
    raise Exception('only [] or {} is allowed!')

  return strippedVar


if __name__ == '__main__':
  xmlDir = os.path.join(os.path.dirname(__file__), 'pali-dict-software-web1version/xml/')
  dpDirName = os.path.join(os.path.dirname(__file__), 'xmlAppEg/')
  savedName = os.path.join(os.path.dirname(__file__), '../jsonPrefixWords')
  groupedSavedName = os.path.join(os.path.dirname(__file__), 'jsonGrouped')
  jsName = os.path.join(os.path.dirname(__file__), '../static/jsonPrefixWords.js')

  if len(sys.argv) != 2:
    usage()
    sys.exit(1)

  if sys.argv[1] == "index":
    buildJSONIndex(xmlDir, savedName)
    sys.exit(0)

  if sys.argv[1] == "group":
    buildWordsGroup(savedName, groupedSavedName)
    sys.exit(0)

  if sys.argv[1] == "stats":
    stats(savedName, groupedSavedName)
    sys.exit(0)

  if sys.argv[1] == "cpdir":
    buildJSONDeployDir(xmlDir, dpDirName, groupedSavedName)
    sys.exit(0)

  if sys.argv[1] == "js":
    buildJS(savedName, groupedSavedName, jsName)
    sys.exit(0)
