#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import csv
import json
import shutil

from variables import getDictWordsCSV1Path
from variables import getDictWordsCSV2Path
from variables import getDictBooksJsonPath
from variables import getDictWordsJsonDir
from variables import jtof


def processWordCSV(csvPath, dicIndex, dstDir):
  with open(csvPath, "r") as wordsCsvfile:
    wordreader = csv.reader(wordsCsvfile, delimiter=',', quotechar='"')
    for row in wordreader:

      if len(row) != 7:
        raise Exception('len(row) != 7')

      if row[0] == 'db_id': continue

      path = os.path.join(dstDir, '%s' % row[4].decode('utf-8').lower())
      print(path)

      if os.path.exists(path):
        # append new data to existing data
        with open(path, 'r') as f:
          data = json.loads(f.read())

        if dicIndex[row[2]][0] == 'zh':
          # convert simplified chinese to traditional chinese
          data.append([row[2], jtof(row[6])])
        else:
          data.append([row[2], row[6]])

        with open(path, 'w') as f:
          f.write(json.dumps(data))
      else:
        # create new data file
        if dicIndex[row[2]][0] == 'zh':
          # convert simplified chinese to traditional chinese
          data = [ [row[2], jtof(row[6])] ]
        else:
          data = [ [row[2], row[6]] ]

        with open(path, 'w') as f:
          f.write(json.dumps(data))


if __name__ == '__main__':
  # read index of dictionary books
  with open(getDictBooksJsonPath(), 'r') as f:
    dicIndex = json.loads(f.read())

  if os.path.exists(getDictWordsJsonDir()):
    shutil.rmtree(getDictWordsJsonDir())
    os.makedirs(getDictWordsJsonDir())
  else:
    os.makedirs(getDictWordsJsonDir())

  processWordCSV(getDictWordsCSV1Path(), dicIndex, getDictWordsJsonDir())
  processWordCSV(getDictWordsCSV2Path(), dicIndex, getDictWordsJsonDir())
