#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json, re


def text2subpath(text):
  subpath = text

  match = re.search(r'^[\d\s()-\.]+', subpath)
  if match:
    subpath = subpath[len(match.group()):]

  match = re.search(r'-\d$', subpath)
  if match:
    subpath = subpath[:-len(match.group())]

  subpath = subpath.lower()

  if subpath.endswith(u'pāḷi'):
    subpath = subpath[:-4]

  if subpath.endswith(u'nikāya'):
    subpath = subpath[:-6]

  if subpath.endswith(u'piṭaka'):
    subpath = subpath[:-6]

  return subpath


def traverseTreeAndSetSubpathProperty(node, space=0):
  if 'conflict' in node:
    subpath = text2subpath(node['text']) + node['conflict']
    del node['conflict']
  else:
    subpath = text2subpath(node['text'])
  #print(' '*space + '[text] => ' + node['text'])
  #print(' '*space + '[subpath]  => ' + subpath)
  # set 'subpath' property of node
  node['subpath'] = subpath

  if 'child' in node:
    subpaths = []
    conflictInfo = {}
    for child in node['child']:
      subpath = text2subpath(child['text'])
      if subpath in subpaths:
        # the same name of subpath already used

        if subpath in conflictInfo:
          conflictInfo[subpath] += 1
        else:
          conflictInfo[subpath] = 2

        child['conflict'] = unicode(conflictInfo[subpath])
        print('\nconflict: ' + subpath)
        #raw_input()

      subpaths.append(subpath)
      traverseTreeAndSetSubpathProperty(child, space+2)

    #raw_input()


if __name__ == '__main__':
  jsonPath = os.path.join(os.path.dirname(__file__), 'treeview.json')

  dstServerJsonPath = os.path.join(os.path.dirname(__file__), '../gae/libs/json/treeviewAll.json')
  #dstClientJsPath = os.path.join(os.path.dirname(__file__), '../app/js/treeviewAllJson.js')
  dstClientJsPath = os.path.join(os.path.dirname(__file__), '../../tipitaka/app/js/treeviewAllJson.js')

  with open(jsonPath, 'r') as f:
    treeviewJson = json.loads(f.read())

  print(type(treeviewJson))
  # set only subpath of tipitaka, no commentries and sub-commentaries
  traverseTreeAndSetSubpathProperty(treeviewJson['child'][0])

  print(treeviewJson['child'][0])

  with open(dstServerJsonPath, 'w') as f:
    f.write(json.dumps(treeviewJson))
  with open(dstClientJsPath, 'w') as f:
    f.write('var treeviewAllJson = ')
    f.write(json.dumps(treeviewJson))
    f.write(';')
