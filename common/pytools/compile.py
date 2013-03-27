#!/usr/bin/env python
# -*- coding:utf-8 -*-

import httplib, urllib, os, json, sys, re

js_common_dir = os.path.join(os.path.dirname(__file__), '../app/js')

dic_js_dir = os.path.join(os.path.dirname(__file__), '../../dictionary/app/js')
dic_compiledJSPath = os.path.join(os.path.dirname(__file__), '../../dictionary/app/all_compiled.js')
dic_uncompiledJSPath = os.path.join(os.path.dirname(__file__), '../../dictionary/app/all_uncompiled.js')

tpk_js_dir = os.path.join(os.path.dirname(__file__), '../../tipitaka/app/js')
tpk_compiledJSPath = os.path.join(os.path.dirname(__file__), '../../tipitaka/app/all_compiled.js')
tpk_uncompiledJSPath = os.path.join(os.path.dirname(__file__), '../../tipitaka/app/all_uncompiled.js')


def getCode(path, flag):
  if path.startswith('/common/js/'):
    with open(os.path.join(js_common_dir, path[11:]), 'r') as f:
      return f.read()

  if path.startswith('/js/'):
    if flag == 'dic':
      jsPath = os.path.join(dic_js_dir, path[4:])
    elif flag == 'tpk':
      jsPath = os.path.join(tpk_js_dir, path[4:])
    else:
      raise Exception('wrong flag')

    with open(jsPath, 'r') as f:
      return f.read()

  raise Exception('should not be here')


def compile2(indexHtmlPath, flag, level):
  code = ''
  with open(indexHtmlPath, 'r') as f:
    for line in f.readlines():
      match = re.search(r'<script src="(.+)"></script>', line)
      if match:
        path = match.group(1)
        if path.startswith('//'):
          continue
        if path.startswith('/js/palidic.js'):
          continue
        if path.startswith('/js/tipitaka.js'):
          continue
        if path.startswith('/common/lib/'):
          continue

        print('combining ' + path + ' ...')
        code += getCode(path, flag)
        code += '\n'

  if flag == 'dic':
    compiledJSPath = dic_compiledJSPath
    uncompiledJSPath = dic_uncompiledJSPath
  elif flag == 'tpk':
    compiledJSPath = tpk_compiledJSPath
    uncompiledJSPath = tpk_uncompiledJSPath
  else:
    raise Exception('wrong flag')

  with open(uncompiledJSPath, 'w') as f:
    f.write(code)

  print('initializing http post request ...')
  params = urllib.urlencode([
      ('js_code', code),
      ('compilation_level', level),
      ('output_format', 'json'),
      ('output_info', 'compiled_code'),
      ('output_info', 'warnings'),
      ('output_info', 'errors'),
      ('output_info', 'statistics'),
    ])

  # Always use the following value for the Content-type header.
  headers = { "Content-type": "application/x-www-form-urlencoded" }
  conn = httplib.HTTPConnection('closure-compiler.appspot.com')
  conn.request('POST', '/compile', params, headers)

  print('sending http post request ...')
  response = conn.getresponse()
  # https://developers.google.com/closure/compiler/docs/api-ref
  data = json.loads(response.read())

  for key in data:
    if key == 'compiledCode':
      with open(compiledJSPath, 'w') as f:
        print('writing compressed code ...')
        f.write(data['compiledCode'])
    else:
      print('%s:' % key)
      recursivePrint(data[key])

  conn.close()


def recursivePrint(data):
  if type(data) is dict:
    for k, v in data.items():
      sys.stdout.write('%s: \t' % k)
      recursivePrint(v)
  elif type(data) is list:
    for item in data:
      recursivePrint(item)
  else:
    print(data)


if __name__ == '__main__':
  if len(sys.argv) == 1:
    level = 'WHITESPACE_ONLY'
  elif sys.argv[1] == 'so':
    level = 'SIMPLE_OPTIMIZATIONS'
  elif sys.argv[1] == 'adv':
    level = 'ADVANCED_OPTIMIZATIONS'
  else:
    level = 'WHITESPACE_ONLY'
  print('compilation_level: %s' % level)

  compile2(os.path.join(os.path.dirname(__file__), '../../dictionary/app/index.html'), 'dic', level)
  compile2(os.path.join(os.path.dirname(__file__), '../../tipitaka/app/index.html'), 'tpk', level)
