#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, urllib2, tarfile, shutil


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


if __name__ == '__main__':
  setupTongWen()
  setupJianfan()
