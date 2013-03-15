#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json

with open(os.path.join(os.path.dirname(__file__), '../common/gae/libs/json/treeviewAll.json'), 'r') as f:
  treeviewData = json.loads(f.read())


def getHtmlTitle(userLocale, reqHandlerName, i18n):
  return ''


def recursivelyCheck(node, path):
  if path[0] is None:
    # check if all items are None
    for subPath in path:
      if subPath is not None:
        return False
    # all items are None => True
    return True

  else:
    for child in node['child']:
      if path[0].decode('utf-8') == child['url']:
        if 'action' in child:
          # check if all remaining items are None
          for subPath in path[1:]:
            if subPath is not None:
              return False
          # all remaining items are None => True
          return True
        else:
          return recursivelyCheck(child, path[1:])

    return False


def isValidCanonPath(path1, path2, path3, path4, path5):
  # rootNode is tipitaka, no commentaris and sub-commentaries
  rootNode = treeviewData['child'][0]
  path = [path1, path2, path3, path4, path5]

  return recursivelyCheck(rootNode, path)


def getCanonPageHtml(urlLocale, path1, path2, path3, path4, path5):
  return '123'


if __name__ == '__main__':
  # for test purpose
  if isValidCanonPath(None, None, None, None, None) is not True:
    print('test failure:')
    print('isValidCanonPath(None, None, None, None, None) is not True')

  if isValidCanonPath(None, None, None, None, '123') is not False:
    print('test failure:')
    print("isValidCanonPath(None, None, None, None, '123') is not False")

  if isValidCanonPath('sutta', 'dīgha', 'sīlakkhandhavagga', 'kūṭadantasuttaṃ', None) is not True:
    print('test failure:')
    print("isValidCanonPath('sutta', 'dīgha', 'sīlakkhandhavagga', 'kūṭadantasuttaṃ', None) is not True")

  if isValidCanonPath('abhidhamma', 'kathāvatthu', 'puggalakathā', None, None) is not True:
    print('test failure:')
    print("isValidCanonPath('abhidhamma', 'kathāvatthu', 'puggalakathā', None, None) is not True")

  if isValidCanonPath('sutta', 'dīgha', None, None, None) is not True:
    print('test failure:')
    print("isValidCanonPath('sutta', 'dīgha', None, None, None) is not True")

  if isValidCanonPath('sutta', None, None, None, None) is not True:
    print('test failure:')
    print("isValidCanonPath('sutta', None, None, None, None) is not True")

  if isValidCanonPath('sutta1', None, None, None, None) is not False:
    print('test failure:')
    print("isValidCanonPath('sutta', None, None, None, None) is not False")

  if isValidCanonPath('abhidhamma', 'kathāvatthu2', 'puggalakathā', None, None) is not False:
    print('test failure:')
    print("isValidCanonPath('abhidhamma', 'kathāvatthu2', 'puggalakathā', None, None) is not False")
