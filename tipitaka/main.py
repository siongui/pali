#!/usr/bin/env python
# -*- coding:utf-8 -*-

import webapp2, jinja2, os, sys, json

sys.path.append(os.path.join(os.path.dirname(__file__), 'gaelibs'))
from url import getHtmlTitle

sys.path.append(os.path.join(os.path.dirname(__file__), 'common/gae/libs'))
from localeUtil import getLocale, parseAcceptLanguage
from misc import isCompiledJS

# zipimport babel and gaepytz
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'common/gae/libs/babel.zip'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'common/gae/libs/pytz.zip'))

from webapp2_extras import i18n

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader([os.path.join(os.path.dirname(__file__), 'app'),
                                    os.path.join(os.path.dirname(__file__), 'app/partials')]),
    extensions=['jinja2.ext.i18n'],
    variable_start_string='{$',
    variable_end_string='$}')

jinja_environment.install_gettext_translations(i18n)


def getCommonTemplateValues(self, urlLocale):
  userLocale = getLocale(urlLocale, self.request.headers.get('accept_language'))
  i18n.get_i18n().set_locale(userLocale)
  template_values = {
    'htmlTitle': getHtmlTitle(userLocale, self.__class__.__name__, i18n),
    'userLocale': userLocale,
    'langQs': json.dumps(parseAcceptLanguage(self.request.headers.get('accept_language'))),
    'urlLocale': urlLocale,
    'isCompiledJS': isCompiledJS(self),
    'urlpath': self.request.path,
    'reqHandlerName': self.__class__.__name__
  }

  return template_values


class MainPage(webapp2.RequestHandler):
  def get(self, urlLocale=None):
    template_values = getCommonTemplateValues(self, urlLocale)
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([
  webapp2.Route(r'/<:|about>', handler=MainPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/', handler=MainPage)],
  debug=True)
