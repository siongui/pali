#!/usr/bin/env python
# -*- coding:utf-8 -*-
# use closure-compiler to shrink JavaScript file size

import os, sys

jsDir = os.path.join(os.path.dirname(__file__), '../static/js/')

compiler = 'java -jar ~/closure-library-read-only/compiler/compiler.jar'

tw1 = '--js ' + jsDir + 'ext/' + 'tongwen_core.js'
tw2 = '--js ' + jsDir + 'ext/' + 'tongwen_table_s2t.js'
tw3 = '--js ' + jsDir + 'ext/' + 'tongwen_table_t2s.js'
tw4 = '--js ' + jsDir + 'ext/' + 'tongwen_table_ps2t.js'
tw5 = '--js ' + jsDir + 'ext/' + 'tongwen_table_pt2s.js'

input_js0 =  '--js ' + jsDir + 'jsonPrefixWords.js'
input_js1 =  '--js ' + jsDir + 'jsonTreeviewToc.js'

input_js2 =  '--js ' + jsDir + 'i18n.js'
input_js3 =  '--js ' + jsDir + 'base.js'
input_js4 =  '--js ' + jsDir + 'movablecolumn.js'
input_js5 =  '--js ' + jsDir + 'data2dom.js'
input_js6 =  '--js ' + jsDir + 'lookup.js'
input_js7 =  '--js ' + jsDir + 'treeview.js'
input_js8 =  '--js ' + jsDir + 'mainview.js'
input_js9 =  '--js ' + jsDir + 'epalitipitaka.js'

output_js_wso = '--js_output_file ' + jsDir + 'epalitipitaka-wso.js'
output_js_spo = '--js_output_file ' + jsDir + 'epalitipitaka-spo.js'
output_js_adv = '--js_output_file ' + jsDir + 'epalitipitaka-adv.js'
output_js_prd = '--js_output_file ' + jsDir + 'epalitipitaka-prd.js'

partial_cmd = '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (compiler, tw1, tw2, tw3, tw4, tw5, input_js0, input_js1, input_js2, input_js3, input_js4, input_js5, input_js6, input_js7, input_js8, input_js9)

wso = '--compilation_level WHITESPACE_ONLY'
spo = '--compilation_level SIMPLE_OPTIMIZATIONS'
adv = '--compilation_level ADVANCED_OPTIMIZATIONS'

def usage():
  print("Usage:")
  print("$ python compile.py help")
  print("$ python compile.py ls")
  print("$ python compile.py rm")
  print("$ python compile.py wso")
  print("$ python compile.py spo")
  print("$ python compile.py adv")
  print("$ python compile.py prd")

if __name__ == '__main__':
  if len(sys.argv) != 2:
    usage()
    sys.exit(1)

  if sys.argv[1] == "help":
    os.system('%s --help' % compiler)
    sys.exit(0)
  elif sys.argv[1] == "ls":
    os.system('ls -al ' + jsDir)
    sys.exit(0)
  elif sys.argv[1] == "rm":
    os.system('rm ' + jsDir + 'epalitipitaka-*.js')
    sys.exit(0)
  elif sys.argv[1] == "wso":
    print(    '%s %s %s' % (partial_cmd, wso, output_js_wso))
    os.system('%s %s %s' % (partial_cmd, wso, output_js_wso))
    sys.exit(0)
  elif sys.argv[1] == "spo":
    print(    '%s %s %s' % (partial_cmd, spo, output_js_spo))
    os.system('%s %s %s' % (partial_cmd, spo, output_js_spo))
    sys.exit(0)
  elif sys.argv[1] == "adv":
    print(    '%s %s %s' % (partial_cmd, adv, output_js_adv))
    os.system('%s %s %s' % (partial_cmd, adv, output_js_adv))
    sys.exit(0)
  elif sys.argv[1] == "prd":
    print(    '%s %s %s' % (partial_cmd, spo, output_js_prd))
    os.system('%s %s %s' % (partial_cmd, spo, output_js_prd))
    sys.exit(0)
  else:
    usage()
    sys.exit(1)
