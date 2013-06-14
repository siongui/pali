#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import csv
import json
import shutil

from variables import getDictBooksCSVPath
from variables import getDictBooksJsonPath
from variables import jtof

"""
In this script, we will build "dicIndex".
The format of dicIndex:

dicIndex = object of key-value pairs, where
  key = id of the dictionary
  value = [cell1, cell2, cell3, cell4], where
    cell1 = language of the dictionary.
            zh: Chinese
            ja: Japanese
            en: English
            vi: Vietnamese
            my: Burmese(Myanmar)
    cell2 = separator, used to get short explanation of the word.
    cell3 = short name of the dictionary
    cell4 = name and author of the dictionary
"""

def processDictionariesBooks():
  with open(getDictBooksCSVPath(), "r") as booksCsvfile:
    bookreader = csv.reader(booksCsvfile, delimiter=',', quotechar='"')
    dicIndex = {}
    for row in bookreader:

      if len(row) != 4:
        raise Exception('len(row) != 4')

      if row[0] == 'b_lang': continue

      # row[1] is the id of the dictionary
      dicIndex[row[1]] = []

      if row[0] == 'C':
        # Chinese and Japanese dictionaries
        if row[1] == 'A':
          # Japanese dictionary
          dicIndex[row[1]].append('ja')
          dicIndex[row[1]].append(' -')
          dicIndex[row[1]].append('《パーリ語辞典》')
          dicIndex[row[1]].append('増補改訂パーリ語辞典  水野弘元著')

        elif row[1] == 'S':
          # Japanese dictionary
          dicIndex[row[1]].append('ja')
          dicIndex[row[1]].append(' -')
          dicIndex[row[1]].append('《パーリ語辞典》')
          dicIndex[row[1]].append('パーリ語辞典  水野弘元著')

        else:
          # Chinese dictionary
          dicIndex[row[1]].append('zh')

          if row[1] == 'D':
            dicIndex[row[1]].append('~')
          elif row[1] == 'H':
            dicIndex[row[1]].append(' -')
          elif row[1] == 'T':
            dicIndex[row[1]].append(' -')
          else:
            dicIndex[row[1]].append('。')

          dicIndex[row[1]].append(jtof(row[2]))
          dicIndex[row[1]].append(jtof(row[3]))

      else:
        # English, Vietnam, Myanmar dictionaries
        if row[1] == 'U' or \
           row[1] == 'Q' or \
           row[1] == 'E':
          # Vietnamese dictionary
          dicIndex[row[1]].append('vi')
          # FIXME: is '。' correct separator?
          dicIndex[row[1]].append('。')

        elif row[1] == 'B' or \
             row[1] == 'K' or \
             row[1] == 'O' or \
             row[1] == 'R':
          # Burmese(Myanmar) dictionary
          dicIndex[row[1]].append('my')
          # FIXME: is '。' correct separator?
          dicIndex[row[1]].append('。')

        else:
          # English dictionary
          dicIndex[row[1]].append('en')
          if row[1] == 'N':
            dicIndex[row[1]].append('<br>')
          elif row[1] == 'C':
            dicIndex[row[1]].append('<br>')
          elif row[1] == 'P':
            dicIndex[row[1]].append('<i>')
          else:
            dicIndex[row[1]].append('。')

        dicIndex[row[1]].append(row[2])
        dicIndex[row[1]].append(row[3])

  return dicIndex


def printInfo(dicIndex):
  import sys
  index = 0
  for key in dicIndex:
    if len(dicIndex[key]) != 4:
      raise Exception('legnth not correct: %s' % key)
    sys.stdout.write(str(index) + ': ')
    sys.stdout.write(key)
    for cell in dicIndex[key]:
      sys.stdout.write(', ' + cell)
    sys.stdout.write('\n')
    index += 1


def writeJsonFile(dicIndex):
  if not os.path.exists(os.path.dirname(getDictBooksJsonPath())):
    os.makedirs(os.path.dirname(getDictBooksJsonPath()))

  with open(getDictBooksJsonPath(), 'w') as f:
    f.write(json.dumps(dicIndex))


if __name__ == '__main__':
  dicIndex = processDictionariesBooks()
  printInfo(dicIndex)
  writeJsonFile(dicIndex)
