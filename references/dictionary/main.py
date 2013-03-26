#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, os, cgi
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'babel.zip'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pytz.zip'))
import webapp2
import jinja2
import urllib
import json
from google.appengine.api import memcache
from webapp2_extras import i18n
from dictionary import lookup, jsonpLookup
from userLocale import getUserLocale
from browse import isValidPrefixAndWord, getPrefixHTML, getWordHTML

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader([os.path.join(os.path.dirname(__file__), 'templates'),
                                  os.path.join(os.path.dirname(__file__), 'templates/js'),
                                  os.path.join(os.path.dirname(__file__), 'templates/google')]),
  extensions=['jinja2.ext.i18n'])

jinja_environment.install_gettext_translations(i18n)

dicPrefixWordLists = json.loads(open('jsonPrefixWords').read())

class MainPage(webapp2.RequestHandler):
  def get(self, prefix=None, word=None):
    locale = getUserLocale(self.request.GET.get('locale'),
                           self.request.headers.get('accept_language'))
    i18n.get_i18n().set_locale(locale)
    #browser = self.request.headers.get('user_agent')

    titleword = u''
    resultDivInnerHTML = None
    if self.request.path.startswith('/browse'):
      if isValidPrefixAndWord(prefix, word, dicPrefixWordLists):
        if (word == None):
          if (prefix != None):
            # build prefix HTML here
            titleword = u'browse words with prefix ' + prefix.decode('utf-8') + u' - '
            resultDivInnerHTML = getPrefixHTML(prefix, dicPrefixWordLists)
        else:
          # build word HTML here
          titleword = word.decode('utf-8') + u' - definition and meaning - '
          resultDivInnerHTML = getWordHTML(word, jsonpLookup(word), i18n)
      else:
        self.error(404)
        self.response.out.write("Page Not Found!")
        return

    compiledBootstrapJS = self.request.GET.get('compiledBootstrapJS')
    if compiledBootstrapJS not in ['yes', 'no']:
      compiledBootstrapJS = None
    if (compiledBootstrapJS == None):
      if os.environ['SERVER_SOFTWARE'].startswith("Development"):
        compiledBootstrapJS = 'no'
      else:
        compiledBootstrapJS = 'yes'

    template_values = {
      'titleword' : titleword,
      'locale' : '%s~%s' % (locale, self.request.headers.get('accept_language')),
      'compiledBootstrapJS' : compiledBootstrapJS,
      'resultDivInnerHTML' : resultDivInnerHTML
    }

    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class Lookup(webapp2.RequestHandler):
  def get(self):
    # http://docs.python.org/library/json.html
    # http://stackoverflow.com/questions/10468553/google-app-engine-json-response-as-rest
    # https://developers.google.com/appengine/docs/python/tools/webapp/redirects
    paliword = cgi.escape(self.request.get('word'))
    self.response.headers['Content-Type'] = 'application/javascript'
    self.response.out.write("%s(%s);" % (self.request.get('callback'), json.dumps(jsonpLookup(paliword))))

  def post(self):
    paliword = cgi.escape(self.request.get('word'))
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(jsonpLookup(paliword)))


app = webapp2.WSGIApplication([('/', MainPage),
                              ('/browse', MainPage),
                              ('/about', MainPage),
                              ('/link', MainPage),
                              (r'/browse/(.*)/(.*)', MainPage),
                              (r'/browse/(.*)', MainPage),
                              ('/lookup', Lookup)],
                              debug=True)
