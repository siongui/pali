#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os


def isTrack(trackQry):
  if isProductionServer():
    if trackQry == 'no':
      return False
    else:
      return True
  else:
    return False


def isGoogleAppEngine():
  try:
    from google.appengine.api import app_identity
    return True
  except:
    return False


def isProductionServer():
  if not isGoogleAppEngine(): return True
  if os.environ['SERVER_SOFTWARE'].startswith("Development"):
    return False
  else:
    return True


def isCompiledJS(jsQry):
  if jsQry == 'yes':
    return True
  elif jsQry == 'no':
    return False
  else:
    return isProductionServer()
