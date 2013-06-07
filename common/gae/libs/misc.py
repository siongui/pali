#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os


def isTrack(trackQry):
  # FIXME: isDevServer is not correctly implemented
  if isDevServer():
    return False
  else:
    if trackQry == 'no':
      return False
    else:
      return True


def isDevServer():
  try:
    from google.appengine.api import app_identity
    # website runs on Google App Engine
    if os.environ['SERVER_SOFTWARE'].startswith("Development"):
      # runs on App Engine Dev Server
      return True
    else:
      # runs on App Engine Production Server
      return False

  except ImportError:
    # website runs not on Google App Engine.
    # FIXME: should figure out some way to check if runs on dev server!
    return False

