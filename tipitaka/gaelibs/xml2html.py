#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from lxml import etree
from translationInfo import getTranslatorSource

paliXmlUrlPrefix = os.path.join(os.path.dirname(__file__), 'romn')
trXmlUrlPrefix = os.path.join(os.path.dirname(__file__), 'translation')

with open(os.path.join(paliXmlUrlPrefix, 'cscd/tipitaka-latn.xsl'), 'r') as f:
  xslt_root = etree.fromstring(f.read())
transform = etree.XSLT(xslt_root)

def getCanonXmlUrl(action):
  return os.path.join(paliXmlUrlPrefix, action)

def getTranslationXmlUrl(xmlFilename, translationLocale, translator):
  code = getTranslatorSource(xmlFilename, translationLocale, translator)
  return os.path.join(trXmlUrlPrefix, '%s/%s/%s' % (
                                       translationLocale, code, xmlFilename))

def paliXslt(xmlUrl):
  root = etree.parse(xmlUrl)
  # transform xml with xslt
  return transform(root)

