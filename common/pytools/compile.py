#!/usr/bin/env python
# -*- coding:utf-8 -*-

import httplib, urllib, os, json, sys

js_common_dir = os.path.join(os.path.dirname(__file__), '../app/js')
js_common_ext_dir = os.path.join(os.path.dirname(__file__), '../app/js/ext')

dic_js_dir = os.path.join(os.path.dirname(__file__), '../../dictionary/app/js')
dic_compiledJSPath = os.path.join(os.path.dirname(__file__), '../../dictionary/app/all_compiled.js')
dic_uncompiledJSPath = os.path.join(os.path.dirname(__file__), '../../dictionary/app/all_uncompiled.js')

tpk_js_dir = os.path.join(os.path.dirname(__file__), '../../tipitaka/app/js')
tpk_compiledJSPath = os.path.join(os.path.dirname(__file__), '../../tipitaka/app/all_compiled.js')
tpk_uncompiledJSPath = os.path.join(os.path.dirname(__file__), '../../tipitaka/app/all_uncompiled.js')


def combindCommonJS():
  code = ''

  for file in os.listdir(js_common_dir):
    if not file.endswith('.js'):
      continue
    path = os.path.join(js_common_dir, file)
    with open(path, 'r') as f:
      print('combining %s ...' % file)
      code += f.read()
      code += '\n'

  # tongwen_table_*.js depends on tongwen_core.js
  # move tongwen_core.js to index 0 of list
  tongwen_files = os.listdir(js_common_ext_dir)
  try:
    core_index = tongwen_files.index('tongwen_core.js')
    tongwen_files.insert(0, tongwen_files.pop(core_index))
  except:
    pass

  for file in tongwen_files:
    if not file.endswith('.js'):
      continue
    path = os.path.join(js_common_ext_dir, file)
    with open(path, 'r') as f:
      print('combining %s ...' % file)
      code += f.read()
      code += '\n'

  return code


def combineJS(flag):
  code = combindCommonJS()
  if flag is 'dic':
    js_dir = dic_js_dir
    uncompiledJSPath = dic_uncompiledJSPath
  if flag is 'tpk':
    js_dir = tpk_js_dir
    uncompiledJSPath = tpk_uncompiledJSPath

  for file in os.listdir(js_dir):
    if not file.endswith('.js'):
      continue
    path = os.path.join(js_dir, file)
    with open(path, 'r') as f:
      print('combining %s ...' % file)
      code += f.read()
      code += '\n'

  with open(uncompiledJSPath, 'w') as f:
    f.write(code)

  return code


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


def compile(flag, level):
  code = combineJS(flag)
  if flag is 'dic':
    compiledJSPath = dic_compiledJSPath
  if flag is 'tpk':
    compiledJSPath = tpk_compiledJSPath

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

  compile('dic', level)
  compile('tpk', level)
