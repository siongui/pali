#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'babel.zip'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pytz.zip'))
import webapp2, jinja2
from webapp2_extras import i18n
from userLocale import getUserLocale
from canonUrl import isValidCanonUrl, getMainViewInnerHTML, getTitleInfo

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader([os.path.join(os.path.dirname(__file__), 'templates')]),
  extensions=['jinja2.ext.i18n'])

jinja_environment.install_gettext_translations(i18n)


class MainPage(webapp2.RequestHandler):
  def get(self):
    locale = getUserLocale(self.request.GET.get('locale'),
                           self.request.headers.get('accept_language'))
    i18n.get_i18n().set_locale(locale)

    titleword = u''
    mainviewDivInnerHTML = None
    if self.request.path.startswith('/canon'):
      if isValidCanonUrl(self.request.path):
        titleword = getTitleInfo(self.request.path)
        mainviewDivInnerHTML = getMainViewInnerHTML(self.request.path)
      else:
        self.error(404)
        self.response.out.write("Page Not Found!")
        return

    devjs = self.request.GET.get('devjs')
    if devjs not in ['yes', 'no']:
      devjs = None
    if devjs == None:
      if os.environ['SERVER_SOFTWARE'].startswith("Development"):
        devjs = 'yes'
      else:
        devjs = 'no'

    template_values = {
      'titleword' : titleword,
      'locale' : '%s~%s' % (locale, self.request.headers.get('accept_language')),
      'mainviewDivInnerHTML': mainviewDivInnerHTML,
      'devjs' : devjs
    }

    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/canon.*', MainPage)],
                              debug=True)
