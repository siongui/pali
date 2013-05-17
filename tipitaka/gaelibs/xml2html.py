#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from lxml import etree
from translationInfo import getTranslatorSource

from google.appengine.ext import ndb
from google.appengine.ext import blobstore

class XmlBlobKey(ndb.Model):
  blob_key = ndb.BlobKeyProperty()

#paliXmlUrlPrefix = os.path.join(os.path.dirname(__file__), 'romn')
trXmlUrlPrefix = os.path.join(os.path.dirname(__file__), 'translation')

xslt_root = etree.parse(blobstore.BlobReader(
    XmlBlobKey.get_by_id('cscd/tipitaka-latn.xsl').blob_key))
transform = etree.XSLT(xslt_root)


def getCanonXmlUrl(action):
  """deprecated"""
  return os.path.join(paliXmlUrlPrefix, action)


def getTranslationXmlUrl(action, translationLocale, translator):
  """Determine the path of translation xml file.

  Returns:
      Path string
  """
  xmlFilename = os.path.basename(action)
  code = getTranslatorSource(xmlFilename, translationLocale, translator)
  return os.path.join(trXmlUrlPrefix, '%s/%s/%s' % (
                                       translationLocale, code, xmlFilename))


def xslt(fileLikeObject):
  root = etree.parse(fileLikeObject)
  # transform xml with xslt
  return transform(root)


def paliXslt(action):
  return xslt(blobstore.BlobReader(XmlBlobKey.get_by_id(action).blob_key))


def translationXslt(action, translationLocale, translator):
  with open(getTranslationXmlUrl(action, translationLocale, translator),
     'r') as f:
    return xslt(f)
