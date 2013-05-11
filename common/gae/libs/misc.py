#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os


def isTrack(self):
  if isProductionServer():
    if self.request.GET.get('track') == 'no':
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
  if os.environ['SERVER_SOFTWARE'].startswith("Development"):
    return False
  else:
    return True


def isCompiledJS(self):
  if self.request.GET.get('js') == 'yes':
    return True
  elif self.request.GET.get('js') == 'no':
    return False
  else:
    return isProductionServer()
