#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
from variables import getInfoFilePath
from variables import getTreeviewJsonPath

"""
tipitaka_toc.xml contains tipitaka, commentaries, and sun-commentaries
toc1.xml contains only tipitaka
"""
separator = u'#@%'


def prettyPrint(obj):
  print(json.dumps(obj, indent=4, separators=(',', ': ')))
  #print(json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))


def printData(stack, node):
  print('-----------------------------')
  prettyPrint(stack)
  print(node)


def isLeafNode(node):
  if 'action' in node:
    return True
  else:
    return False


def getNodeDict(line):
  array = line.split(separator)
  if len(array) == 3:
    # leaf node
    depth = int(array[0])
    text = array[1]
    action = array[2]
    return {'depth': depth, 'text': text, 'action': action}
  else:
    # not leaf node
    depth = int(array[0])
    text = array[1]
    return {'depth': depth, 'text': text}


def updateStack(stack, node):
  #printData(stack, node, currentDepth)
  if stack[-1]['depth'] < node['depth']:
    if isLeafNode(node):
      node.pop('depth')
      stack[-1]['child'].append(node)
    else:
      node['child'] = []
      stack.append(node)
    return stack

  elif stack[-1]['depth'] > node['depth']:
    deepestNode = stack.pop()
    deepestNode.pop('depth')
    stack[-1]['child'].append(deepestNode)
    return updateStack(stack, node)

  else:
    # stack[-1]['dpeth'] = node['depth']
    deepestNode = stack.pop()
    deepestNode.pop('depth')
    stack[-1]['child'].append(deepestNode)
    if not isLeafNode(node):
      node['child'] = []
    stack.append(node)
    return stack


def infoFile2TreeviewData(path):
  rootNode = {'child': [], 'depth': 0}
  stack = [rootNode]
  with open(path, 'r') as f:
    for line in f.readlines():
      # remove '\n' and decode as utf-8
      line = line[:-1].decode('utf-8')
      # each line represents one node
      node = getNodeDict(line)
      stack = updateStack(stack, node)
  return rootNode


if __name__ == '__main__':
  treeviewData = infoFile2TreeviewData(getInfoFilePath())

  with open(getTreeviewJsonPath(), 'w') as f:
    f.write(json.dumps(treeviewData))

  prettyPrint(treeviewData)
