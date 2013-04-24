#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json, re


def text2subpath(text):
  subpath = text

  # remove leading un-needed characters
  match = re.search(r'^[\d\s()-\.]+', subpath)
  if match:
    subpath = subpath[len(match.group()):]

  # remove trailing un-needed characters
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

  if subpath.endswith(u'piṭaka (aṭṭhakathā)'):
    subpath = subpath[:-19]

  if subpath.endswith(u'-aṭṭhakathā'):
    if subpath.endswith(u'kaṇḍa-aṭṭhakathā'):
      subpath = subpath[:-16]
    else:
      subpath = subpath[:-11]

  if subpath.endswith(u'nikāya (aṭṭhakathā)'):
    if subpath.endswith(u' nikāya (aṭṭhakathā)'):
      subpath = subpath[:-20]
    else:
      subpath = subpath[:-19]

  if subpath.endswith(u'piṭaka (ṭīkā)'):
    subpath = subpath[:-13]

  if subpath.endswith(u'nikāya (ṭīkā)'):
    subpath = subpath[:-13]

  if subpath.endswith(u'-mūlaṭīkā'):
    subpath = subpath[:-9]

  if subpath.endswith(u'-ṭīkā'):
    subpath = subpath[:-5]

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

  dstServerJsonPath = os.path.join(os.path.dirname(__file__), '../../tipitaka/gaelibs/json/treeviewAll.json')
  dstClientJsPath = os.path.join(os.path.dirname(__file__), '../../tipitaka/app/js/treeviewAllJson-service.js')

  with open(jsonPath, 'r') as f:
    treeviewJson = json.loads(f.read())

  # set subpath of Tipiṭaka, commentries, and sub-commentaries
  for child in treeviewJson['child']:
    traverseTreeAndSetSubpathProperty(child)

  # set subpath of Tipiṭaka (Mūla) as canon
  treeviewJson['child'][0]['subpath'] = 'canon'

  print(treeviewJson)

  if not os.path.exists(os.path.dirname(dstServerJsonPath)):
    os.makedirs(os.path.dirname(dstServerJsonPath))
  with open(dstServerJsonPath, 'w') as f:
    f.write(json.dumps(treeviewJson))

  with open(dstClientJsPath, 'w') as f:
    f.write("angular.module('pali.treeviewAllJson', []).\n")
    f.write("  factory('treeviewAllJson', [function() {\n")
    f.write("    var treeviewData = ")
    f.write(json.dumps(treeviewJson))
    f.write(";\n")
    f.write("    var serviceInstance = { all: treeviewData, tpk: treeviewData['child'][0] };\n")
    f.write("    return serviceInstance;\n")
    f.write("  }]);\n")
