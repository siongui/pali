#!/usr/bin/env python
# -*- coding:utf-8 -*-

# google search keyword: html code multiple file upload
# http://davidwalsh.name/multiple-file-upload
# google search keyword: gae receive multiple file upload
# http://stackoverflow.com/questions/1503526/receive-multi-file-post-with-google-app-engine

import webapp2
import os, cgi
import jinja2
from dictionary import decodeXML, storeToNDB

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


class AdminPage(webapp2.RequestHandler):
  def get(self):
    template_values = {
    }

    template = jinja_environment.get_template('admin.html')
    self.response.out.write(template.render(template_values))


class AddFilePage(webapp2.RequestHandler):
  def post(self):
    result = u''
    uploadedContents = u''
    for file_data in self.request.POST.getall('filesToUpload[]'):
      # file name: file_data.filename ; file content: file_data.value
      result += storeToNDB(file_data.filename, file_data.value)
      result += u'</br>'
#      uploadedContents += decodeXML(file_data.filename, file_data.value)

    template_values = {
      'result': result,
      'uploadedContents': uploadedContents,
    }

    template = jinja_environment.get_template('result.html')
    self.response.out.write(template.render(template_values))



app = webapp2.WSGIApplication([('/admin/', AdminPage),
                              ('/admin/addfile', AddFilePage)],
                              debug=True)
