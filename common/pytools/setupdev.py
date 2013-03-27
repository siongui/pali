#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, urllib2, tarfile, shutil, zipfile

"""
$PALI_DIR is the dir of git clone https://github.com/siongui/pali.git
Manual setup (for reference):
1. setup TongWen:
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

2. setup jianfan:
```bash
  wget https://python-jianfan.googlecode.com/files/jianfan-0.0.1.tar.gz
  tar xvzf jianfan-0.0.1.tar.gz
  mv jianfan-0.0.1/jianfan $PALI_DIR/common/gae/libs/
  rm -rf jianfan-0.0.1
```

3. create symbolic links:
```bash
  cd $PALI_DIR/dictionary
  ln -s ../common/ common
  ln -s ../common/locale/ locale
  cd $PALI_DIR/tipitaka
  ln -s ../common/ common
  ln -s ../common/locale/ locale
```

4. setup Babel:
```bash
  wget http://ftp.edgewall.com/pub/babel/Babel-0.9.6.zip
  unzip Babel-0.9.6.zip
  cd Babel-0.9.6/
  zip -r babel.zip babel/
  mv babel.zip $PALI_DIR/common/gae/libs/
```

5. setup gaepytz:
```bash
  wget https://pypi.python.org/packages/source/g/gaepytz/gaepytz-2011h.zip#md5=0f130ef491509775b5ed8c5f62bf66fb
  unzip gaepytz-2011h.zip
  cd ../gaepytz-2011h/
  zip -r pytz.zip pytz/
  mv pytz.zip $PALI_DIR/common/gae/libs/
```
"""


def download(url, path):
  print('downloading %s ...' % url)
  response = urllib2.urlopen(url)
  with open(path, 'w') as f:
    f.write(response.read())
  print('%s saved!' % path)


def setupTongWen():
  jsExtDir = os.path.join(os.path.dirname(__file__), '../app/js/ext')
  if not os.path.exists(jsExtDir):
    os.makedirs(jsExtDir)

  TongWenUrlPrefix = 'http://tongwen.openfoundry.org/src/web'
  TongWen_files = ['tongwen_core.js', 'tongwen_table_s2t.js', 'tongwen_table_t2s.js', 'tongwen_table_ps2t.js', 'tongwen_table_pt2s.js']

  for file in TongWen_files:
    url = os.path.join(TongWenUrlPrefix, file)
    path = os.path.join(jsExtDir, file)
    download(url, path)


def setupJianfan():
  url = 'https://python-jianfan.googlecode.com/files/jianfan-0.0.1.tar.gz'
  path = os.path.join(os.path.dirname(__file__), 'jianfan-0.0.1.tar.gz')
  pkgpath = os.path.join(os.path.dirname(__file__), 'jianfan-0.0.1')
  libpath = os.path.join(os.path.dirname(__file__), 'jianfan-0.0.1/jianfan')
  dstpath = os.path.join(os.path.dirname(__file__), '../gae/libs/jianfan')

  if os.path.exists(pkgpath):
    shutil.rmtree(pkgpath)
  if os.path.exists(dstpath):
    shutil.rmtree(dstpath)

  download(url, path)
  with tarfile.open(path) as tar:
    tar.extractall()

  shutil.move(libpath, dstpath)
  shutil.rmtree(pkgpath)
  os.chmod(dstpath, 0o755)
  for file in os.listdir(dstpath):
    fpath = os.path.join(dstpath, file)
    os.chmod(fpath, 0o644)
  os.remove(path)


def ln(source, link_name):
  if os.path.islink(link_name):
    os.unlink(link_name)
  os.symlink(source, link_name)


def setupSymlinks():
  os.chdir(os.path.join(os.path.dirname(__file__), '../../tipitaka'))
  ln('../common/', 'common')
  ln('../common/locale/', 'locale')
  os.chdir('../dictionary')
  ln('../common/', 'common')
  ln('../common/locale/', 'locale')


def setupXmls():
  dataUrl = 'https://github.com/siongui/data/archive/master.zip'
  path = os.path.join(os.path.dirname(__file__), 'master.zip')
  commonDirPath = os.path.join(os.path.dirname(__file__), '..')

  if not os.path.exists(path):
    download(dataUrl, path)

  with zipfile.ZipFile(path, 'r') as zf:
    for name in zf.namelist():
      if name.startswith('data-master/pali/common/translation/'):
        (dirname, filename) = os.path.split(name)
        dstDir = os.path.join(commonDirPath, dirname.replace('data-master/pali/common/', ''))
        dstPath = os.path.join(dstDir, filename)

        if filename == '':
          # directory
          if not os.path.exists(dstDir):
            print("creating " + dstDir)
            os.mkdir(dstDir)
        else:
          print("Decompressing " + name + " to " + dstPath)
          # file
          with open(dstPath, 'w') as f:
            f.write(zf.read(name))

      if name.startswith('data-master/pali/common/romn/'):
        (dirname, filename) = os.path.split(name)
        dstDir = os.path.join(commonDirPath, dirname.replace('data-master/pali/common/', ''))
        dstPath = os.path.join(dstDir, filename)

        if filename == '':
          # directory
          if not os.path.exists(dstDir):
            print("creating " + dstDir)
            os.mkdir(dstDir)
        else:
          # file
          if 'toc' not in filename:
            if 'mul' in filename or filename.startswith('tipitaka-latn') or filename.startswith('s0518m.nrf') or filename.startswith('s0520m.nrf'):
              print("Decompressing " + name + " to " + dstPath)
              with open(dstPath, 'w') as f:
                f.write(zf.read(name))


def setupBabel():
  babelUrl = 'http://ftp.edgewall.com/pub/babel/Babel-0.9.6.zip'
  babelZipPath = os.path.join(os.path.dirname(__file__), 'Babel-0.9.6.zip')

  if not os.path.exists(babelZipPath):
    download(babelUrl, babelZipPath)

  with zipfile.ZipFile(babelZipPath, 'r') as zf:
    for name in zf.namelist():
      print(name)


def setupAll():
  pass


if __name__ == '__main__':
  setupTongWen()
  setupJianfan()
  setupSymlinks()
  setupXmls()
  #setupBabel()
  #setupAll()
