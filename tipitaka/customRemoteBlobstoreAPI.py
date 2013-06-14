#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
https://developers.google.com/appengine/docs/python/tools/devserver#Using_the_Datastore
http://stackoverflow.com/questions/12447489/how-to-upload-data-to-local-datastore?lq=1
http://stackoverflow.com/questions/2817733/use-gae-remote-api-with-local-dev-installation
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'common/pylib'))
import web

from google.appengine.ext import ndb
from google.appengine.api import files
import json
import base64

class XmlBlobKey(ndb.Model):
  blob_key = ndb.BlobKeyProperty()

urls = (
#  "/uploadOver1mb", "upload",
  "/customRemoteBlobstoreAPI", "customRemoteBlobstoreAPIHandler",
)

class upload:
  """deprecated"""
  def GET(self):
    return """<html><head></head><body>
        <form method="POST" enctype="multipart/form-data" action="">
        <input type="file" name="myfile" />
        <br/>
        <input type="submit" />
        </form>
        </body></html>"""
  def POST(self):
    """Receive multipart/form-data HTTP file POST.
    """
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


class customRemoteBlobstoreAPIHandler:
  def POST(self):
    """Receive HTTP POST (json-format data), and store data to blobstore.
    """
    data = json.loads(web.data())

    # Create the file
    # set filename property in BlobStore
    # http://stackoverflow.com/questions/5697844/how-to-set-filename-property-in-blobstore
    file_name = files.blobstore.create(mime_type='application/octet-stream',
        _blobinfo_uploaded_filename=data['key'])

    # Open the file and write to it
    with files.open(file_name, 'a') as f:
      f.write(base64.b64decode(data['payload']))

    # Finalize the file. Do this before attempting to read it.
    files.finalize(file_name)

    # Get the file's blob key
    blob_key = files.blobstore.get_blob_key(file_name)

    # store blob_key in datastore
    XmlBlobKey(id=data['key'], blob_key=blob_key).put()

    return 'OK<br />%s<br />%s' % (data['key'], blob_key)


app = web.application(urls, globals())
app = app.gaerun()
