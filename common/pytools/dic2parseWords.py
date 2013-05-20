#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import csv
import json
import shutil

try:
  import pyopencc
  cc = pyopencc.OpenCC('zhs2zht.ini')
  jtof = cc.convert
except:
  print('cannot import opencc, import jianfan')
  sys.path.append(os.path.join(os.path.dirname(__file__), '../gae/libs'))
  from jianfan import jtof


dictBooksJsonPath = os.path.join(os.path.dirname(__file__), 'books.json')
with open(dictBooksJsonPath, 'r') as f:
  dicIndex = json.loads(f.read())


dictWordsCSV1Path = os.path.join(os.path.dirname(__file__),
    "../../../data/pali/common/dictionary/dict_words_1.csv")
dictWordsCSV2Path = os.path.join(os.path.dirname(__file__),
    "../../../data/pali/common/dictionary/dict_words_2.csv")

dictWordsJsonDir = os.path.join(os.path.dirname(__file__), 'paliwords')


def processWordCSV(csvPath):
  with open(csvPath, "r") as wordsCsvfile:
    wordreader = csv.reader(wordsCsvfile, delimiter=',', quotechar='"')
    for row in wordreader:

      if len(row) != 7:
        raise Exception('len(row) != 7')

      if row[0] == 'db_id': continue

      """
      print(dicIndex[row[2]]['locale'])
      print(dicIndex[row[2]]['data'][2])
      print(dicIndex[row[2]]['data'][3])
      print(row[4])
      print(row[6])
      """

      #path = os.path.join(output_dir, '%s.json' % 
      path = os.path.join(dictWordsJsonDir, '%s' % 
          row[4].decode('utf-8').lower())
      print(path)
      #print([dicIndex[row[2]]['data'][1], row[6]])

      if os.path.exists(path):
        # append new data to existing data
        with open(path, 'r') as f:
          data = json.loads(f.read())

        if dicIndex[row[2]]['locale'] == 'zh':
          data.append([dicIndex[row[2]]['data'][1], jtof(row[6])])
        else:
          data.append([dicIndex[row[2]]['data'][1], row[6]])

        with open(path, 'w') as f:
          f.write(json.dumps(data))
      else:
        # create new data file
        if dicIndex[row[2]]['locale'] == 'zh':
          data = [ [dicIndex[row[2]]['data'][1], jtof(row[6])] ]
        else:
          data = [ [dicIndex[row[2]]['data'][1], row[6]] ]

        with open(path, 'w') as f:
          f.write(json.dumps(data))


if __name__ == '__main__':
  if os.path.exists(dictWordsJsonDir):
    shutil.rmtree(dictWordsJsonDir)
    os.makedirs(dictWordsJsonDir)
  else:
    os.makedirs(dictWordsJsonDir)

  processWordCSV(dictWordsCSV1Path)
  processWordCSV(dictWordsCSV2Path)
