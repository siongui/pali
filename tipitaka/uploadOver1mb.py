#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'common/gae/libs'))
import web

from google.appengine.ext import ndb
from google.appengine.api import files

class XmlBlobKey(ndb.Model):
  blob_key = ndb.BlobKeyProperty()

urls = (
  "/uploadOver1mb", "upload",
)

class upload:
  def GET(self):
    return """<html><head></head><body>
        <form method="POST" enctype="multipart/form-data" action="">
        <input type="file" name="myfile" />
        <br/>
        <input type="submit" />
        </form>
        </body></html>"""
  def POST(self):
    x = web.input(myfile={})
    key = 'cscd/' + x['myfile'].filename
    #Xml(id=key, content=x['myfile'].value).put()
    # Create the file
    file_name = files.blobstore.create(mime_type='application/octet-stream')

    # Open the file and write to it
    with files.open(file_name, 'a') as f:
      f.write(x['myfile'].value)

    # Finalize the file. Do this before attempting to read it.
    files.finalize(file_name)

    # Get the file's blob key
    blob_key = files.blobstore.get_blob_key(file_name)

    XmlBlobKey(id=key, blob_key=blob_key).put()

    return '%s <br />\n %s' % (key, blob_key)


app = web.application(urls, globals())
app = app.gaerun()
