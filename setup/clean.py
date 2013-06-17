#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

from i18nUtils import locales

if __name__ == '__main__':
  for locale in locales:
    if locale == 'zh_CN' or locale == 'en_US':
      continue

    path = os.path.join(os.path.dirname(__file__),
        '../common/locale/%s/LC_MESSAGES/messages.po' % locale)

    os.system('git checkout %s' % path)
