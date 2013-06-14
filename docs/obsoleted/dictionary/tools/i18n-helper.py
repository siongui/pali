#!/usr/bin/env python
# -*- coding:utf-8 -*-

# http://wiki.maemo.org/Internationalize_a_Python_application

import os, sys


if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("only one argument accepted!")
    print("Usage:")
    print("$ python i18n-helper.py pot")
    print("$ python i18n-helper.py po")
    print("$ python i18n-helper.py mo")
    print("$ python i19n-helper.py update")
    sys.exit(1)

  if sys.argv[1] == "pot":
    os.system('xgettext --from-code=UTF-8 --keyword=_ --output=locale/messages.pot `find ./templates -name "*.html"` templates/js/potI18N.js')
    os.system('sed -i "s/charset=CHARSET/charset=utf-8/g" locale/messages.pot')
    sys.exit(0)

  """
  if sys.argv[1] == "po":
    os.system('pybabel init -l en_US -d ./locale -i ./locale/messages.pot')
    os.system('pybabel init -l zh_TW -d ./locale -i ./locale/messages.pot')
    os.system('pybabel init -l zh_CN -d ./locale -i ./locale/messages.pot')
    sys.exit(0)
  """

  if sys.argv[1] == "mo":
    os.system('pybabel compile -f -d ./locale')
    sys.exit(0)

  if sys.argv[1] == "update":
    os.system('pybabel update -l en_US -d ./locale -i ./locale/messages.pot')
    os.system('pybabel update -l zh_TW -d ./locale -i ./locale/messages.pot')
    os.system('pybabel update -l zh_CN -d ./locale -i ./locale/messages.pot')
    sys.exit(0)

  print("Usage:")
  print("$ python i18n-helper.py pot")
  print("$ python i18n-helper.py po")
  print("$ python i18n-helper.py mo")
  print("$ python i19n-helper.py update")
  sys.exit(1)
