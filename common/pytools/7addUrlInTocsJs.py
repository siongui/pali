#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json, re


def text2Url(text):
  url = text

  match = re.search(r'^[\d\s()-\.]+', url)
  if match:
    url = url[len(match.group()):]

  match = re.search(r'-\d$', url)
  if match:
    url = url[:-len(match.group())]

  url = url.lower()

  if url.endswith(u'pāḷi'):
    url = url[:-4]

  if url.endswith(u'nikāya'):
    url = url[:-6]

  if url.endswith(u'piṭaka'):
    url = url[:-6]

  return url


def traverseTreeAndSetUrlProperty(node, space=0):
  if 'conflict' in node:
    url = text2Url(node['text']) + node['conflict']
    del node['conflict']
  else:
    url = text2Url(node['text'])
  #print(' '*space + '[text] => ' + node['text'])
  #print(' '*space + '[url]  => ' + url)
  # set 'url' property of node
  node['url'] = url

  if 'child' in node:
    urls = []
    conflictInfo = {}
    for child in node['child']:
      url = text2Url(child['text'])
      if url in urls:
        # the same name of url already used

        if url in conflictInfo:
          conflictInfo[url] += 1
        else:
          conflictInfo[url] = 2

        child['conflict'] = unicode(conflictInfo[url])
        print('\nconflict: ' + url)
        #raw_input()

      urls.append(url)
      traverseTreeAndSetUrlProperty(child, space+2)

    #raw_input()


if __name__ == '__main__':
  serverJsonPath = os.path.join(os.path.dirname(__file__), '../gae/libs/json/treeview.json')
  #clientJsPath = os.path.join(os.path.dirname(__file__), '../app/js/treeviewJson.js')
  clientJsPath = os.path.join(os.path.dirname(__file__), '../../tipitaka/app/js/treeviewJson.js')

  dstServerJsonPath = os.path.join(os.path.dirname(__file__), '../gae/libs/json/treeviewAll.json')
  #dstClientJsPath = os.path.join(os.path.dirname(__file__), '../app/js/treeviewAllJson.js')
  dstClientJsPath = os.path.join(os.path.dirname(__file__), '../../tipitaka/app/js/treeviewAllJson.js')

  with open(serverJsonPath, 'r') as f:
    treeviewJson = json.loads(f.read())

  print(type(treeviewJson))
  # set only url of tipitaka, no commentries and sub-commentaries
  traverseTreeAndSetUrlProperty(treeviewJson['child'][0])

  print(treeviewJson['child'][0])

  with open(dstServerJsonPath, 'w') as f:
    f.write(json.dumps(treeviewJson))
  with open(dstClientJsPath, 'w') as f:
    f.write('var treeviewAllJson = ')
    f.write(json.dumps(treeviewJson))
    f.write(';')
