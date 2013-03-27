#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys
import json

# @see https://developers.google.com/appengine/docs/python/runtime#Quotas_and_Limits
# maximum total number of files (app files and static files): 10,000 per directory
# @see https://developers.google.com/appengine/docs/quotas#Deployments
# An application is limited to 10,000 uploaded files per version.

if __name__ == '__main__':
  srcJsonFile = os.path.join(os.path.dirname(__file__), '../gae/libs/json/dicPrefixWordLists.json')
  dstJsonFile = os.path.join(os.path.dirname(__file__), '../gae/libs/json/dicPrefixGroup.json')

  if not os.path.exists(srcJsonFile):
    print(srcJsonFile + ' does not exist!')
    sys.exit(1)

  with open(srcJsonFile, 'r') as f:
    dicPrefixWordLists = json.loads(f.read())

  total = 0
  group = 0
  dicPrefixGroup = {}
  for key in dicPrefixWordLists:
    number = len(dicPrefixWordLists[key])
    total += number

    if total > 9990:
      total = number
      group += 1

    dicPrefixGroup[key.encode('utf-8')] = group

  with open(dstJsonFile, 'w') as f:
    f.write(json.dumps(dicPrefixGroup))

  # calculate and print statistics
  totalNum = 0
  groupNum = {}
  for key in dicPrefixWordLists:
    number = len(dicPrefixWordLists[key])
    totalNum += number
    group = dicPrefixGroup[key.encode('utf-8')]
    if group in groupNum:
      groupNum[group] += number
    else:
      groupNum[group] = number
    print('prefix: %s\t#: %d    \tgroup: %d' % (key, number, group))

  for key in groupNum:
    print('group %d:\t%d (<10,000)' % (key, groupNum[key]))
  print("total number:\t%d" % totalNum)
