#!/usr/bin/env python
# -*- coding:utf-8 -*-
# use closure-compiler to shrink JavaScript file size

import os, sys

compiler = 'java -jar ~/closure-library-read-only/compiler/compiler.jar'

input_bootstrap = '--js templates/js/bootstrap.js'
output_bootstrap_wso = '--js_output_file templates/js/bootstrap-wso.js'
output_bootstrap_spo = '--js_output_file templates/js/bootstrap-spo.js'
output_bootstrap_adv = '--js_output_file templates/js/bootstrap-adv.js'
output_bootstrap_prd = '--js_output_file templates/js/bootstrap-prd.js'

input_base = '--js static/js/base.js'
input_js1 =  '--js static/js/customevent.js'
input_js2 =  '--js static/js/data2dom.js'
input_js3 =  '--js static/js/dropdown.js'
input_js4 =  '--js static/js/draggable.js'
input_js5 =  '--js static/js/inputsuggest.js'
input_js6 =  '--js static/js/lookup.js'
input_js7 =  '--js static/js/palidict.js'
output_js_wso = '--js_output_file static/js/pali-wso.js'
output_js_spo = '--js_output_file static/js/pali-spo.js'
output_js_adv = '--js_output_file static/js/pali-adv.js'
output_js_prd = '--js_output_file static/js/pali-prd.js'

partial_cmd = '%s %s %s %s %s %s %s %s %s' % (compiler, input_base, input_js1, input_js2, input_js3, input_js4, input_js5, input_js6, input_js7)

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
    os.system('ls -al static/js/')
    os.system('ls -al templates/js/')
    sys.exit(0)
  elif sys.argv[1] == "rm":
    os.system('rm static/js/pali-*.js')
    os.system('rm templates/js/bootstrap-*.js')
    sys.exit(0)
  elif sys.argv[1] == "wso":
    print(    '%s %s %s %s' % (compiler, wso, input_bootstrap, output_bootstrap_wso))
    os.system('%s %s %s %s' % (compiler, wso, input_bootstrap, output_bootstrap_wso))
    print(    '%s %s %s' % (partial_cmd, wso, output_js_wso))
    os.system('%s %s %s' % (partial_cmd, wso, output_js_wso))
    sys.exit(0)
  elif sys.argv[1] == "spo":
    print(    '%s %s %s %s' % (compiler, spo, input_bootstrap, output_bootstrap_spo))
    os.system('%s %s %s %s' % (compiler, spo, input_bootstrap, output_bootstrap_spo))
    print(    '%s %s %s' % (partial_cmd, spo, output_js_spo))
    os.system('%s %s %s' % (partial_cmd, spo, output_js_spo))
    sys.exit(0)
  elif sys.argv[1] == "adv":
    print(    '%s %s %s %s' % (compiler, adv, input_bootstrap, output_bootstrap_adv))
    os.system('%s %s %s %s' % (compiler, adv, input_bootstrap, output_bootstrap_adv))
    print(    '%s %s %s' % (partial_cmd, adv, output_js_adv))
    os.system('%s %s %s' % (partial_cmd, adv, output_js_adv))
    sys.exit(0)
  elif sys.argv[1] == "prd":
    print(    '%s %s %s %s' % (compiler, spo, input_bootstrap, output_bootstrap_prd))
    os.system('%s %s %s %s' % (compiler, spo, input_bootstrap, output_bootstrap_prd))
    print(    '%s %s %s' % (partial_cmd, spo, output_js_prd))
    os.system('%s %s %s' % (partial_cmd, spo, output_js_prd))
    sys.exit(0)
  else:
    usage()
    sys.exit(1)
