#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os 
import shutil

"""
$PALI_DIR is the dir of git clone https://github.com/siongui/pali.git
Manual setup (for reference):
1. setup TongWen (deprecated):
```bash
  cd $PALI_DIR
  mkdir -p common/app/js/ext
  cd common/app/js/ext/
  wget http://tongwen.openfoundry.org/src/web/tongwen_core.js
  wget http://tongwen.openfoundry.org/src/web/tongwen_table_s2t.js
  wget http://tongwen.openfoundry.org/src/web/tongwen_table_t2s.js
  wget http://tongwen.openfoundry.org/src/web/tongwen_table_ps2t.js
  wget http://tongwen.openfoundry.org/src/web/tongwen_table_pt2s.js
```

2. setup jianfan (deprecated):
```bash
  wget https://python-jianfan.googlecode.com/files/jianfan-0.0.2.zip
  unzip jianfan-0.0.2.zip
  mv jianfan-0.0.2/jianfan $PALI_DIR/common/gae/libs/
  rm -rf jianfan-0.0.2
```

3. create symbolic links:
```bash
  cd $PALI_DIR/tipitaka
  ln -s ../common/ common

  cd $PALI_DIR/tipitaka/gaelibs
  ln -s ../../../data/pali/common/translation/ translation

  cd $PALI_DIR/dictionary
  ln -s ../common/ common

  cd $PALI_DIR/common/gae/libs
  ln -s ../../../../data/pali/common/gae/libs/jianfan/ jianfan

  cd $PALI_DIR/common/app/js
  ln -s ../../../../data/pali/common/app/js/ext/ ext
```
"""


def ln(source, link_name):
  if os.path.islink(link_name):
    os.unlink(link_name)
  os.symlink(source, link_name)


def setupSymlinks():
  # enter tipitaka dir
  os.chdir(os.path.join(os.path.dirname(__file__), '../../tipitaka'))
  ln('../common/', 'common')
  os.chdir('gaelibs')
  ln('../../../data/pali/common/translation/', 'translation')
  # enter dictionary dir
  os.chdir('../../dictionary')
  ln('../common/', 'common')
  # enter common dir
  os.chdir('../common/gae/libs')
  ln('../../../../data/pali/common/gae/libs/jianfan/', 'jianfan')
  os.chdir('../../app/js')
  ln('../../../../data/pali/common/app/js/ext/', 'ext')


if __name__ == '__main__':
  tipitakaLatnCssPath = os.path.join(os.path.dirname(__file__),
      '../../../data/pali/common/romn/cscd/tipitaka-latn.css')
  dstPath = os.path.join(os.path.dirname(__file__),
      '../../tipitaka/app/css/tipitaka-latn.css')
  shutil.copyfile(tipitakaLatnCssPath, dstPath)

  setupSymlinks()
