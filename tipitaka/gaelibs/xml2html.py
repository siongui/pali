#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from lxml import etree
from translationInfo import getTranslatorSource


import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../common/gae/libs'))
from misc import isGoogleAppEngine
from misc import isProductionServer

if isGoogleAppEngine():
  if isProductionServer():
    paliXmlUrlPrefix = u'http://epalitipitaka.appspot.com/romn/'
    trXmlUrlPrefix = u'http://epalitipitaka.appspot.com/translation/'
  else:
    #paliXmlUrlPrefix = os.path.join(os.path.dirname(__file__), 'romn')
    #trXmlUrlPrefix = os.path.join(os.path.dirname(__file__), 'translation')
    paliXmlUrlPrefix = u'http://localhost:8080/romn/'
    trXmlUrlPrefix = u'http://localhost:8080/translation/'
else:
  # add amazon ec2 support here
  raise Exception('currently only Google App Engine is supported')


if isGoogleAppEngine():
  xslt_root = etree.parse(os.path.join(
                paliXmlUrlPrefix, 'cscd/tipitaka-latn.xsl'))
  transform = etree.XSLT(xslt_root)
else:
  # add amazon ec2 support here
  """
  with open(os.path.join(paliXmlUrlPrefix, 'cscd/tipitaka-latn.xsl'), 'r') as f:
    xslt_root = etree.fromstring(f.read())
  transform = etree.XSLT(xslt_root)
  """
  raise Exception('currently only Google App Engine is supported')


def getCanonXmlUrl(action):
  return os.path.join(paliXmlUrlPrefix, action)

def getTranslationXmlUrl(action, translationLocale, translator):
  xmlFilename = os.path.basename(action)
  code = getTranslatorSource(xmlFilename, translationLocale, translator)
  return os.path.join(trXmlUrlPrefix, '%s/%s/%s' % (
                                       translationLocale, code, xmlFilename))

def xslt(url):
  root = etree.parse(url)
  # transform xml with xslt
  return transform(root)


def paliXslt(action):
  return xslt(getCanonXmlUrl(action))


def translationXslt(action, translationLocale, translator):
  return xslt(getTranslationXmlUrl(action, translationLocale, translator))
