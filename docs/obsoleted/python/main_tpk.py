#!/usr/bin/env python
# -*- coding:utf-8 -*-

# deprecated! Now use web.py framework!

import webapp2, jinja2, os, sys, json
from  webapp2_extras.routes import PathPrefixRoute

sys.path.append(os.path.join(os.path.dirname(__file__), 'pylib'))
from url import getAllLocalesTranslationsHtml
from url import checkPath

sys.path.append(os.path.join(os.path.dirname(__file__), 'common/pylib'))
from localeUtil import getLocale
from localeUtil import parseAcceptLanguage
from misc import isDevServer
from misc import isTrack
import i18n

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
      [os.path.join(os.path.dirname(__file__), 'app'),
       os.path.join(os.path.dirname(__file__), 'app/css'),
       os.path.join(os.path.dirname(__file__), 'app/partials')]),
    extensions=['jinja2.ext.i18n'],
    variable_start_string='{$',
    variable_end_string='$}')

jinja_environment.install_gettext_translations(i18n)


def getCommonTemplateValues(self, urlLocale, userLocale):
  i18n.setLocale(userLocale)
  template_values = {
    'htmlTitle': u'',
    'userLocale': userLocale,
    'langQs': json.dumps(parseAcceptLanguage(self.request.headers.get('accept_language'))),
    'urlLocale': urlLocale,
    'isTrack': isTrack(self.request.GET.get('track')),
    'isDevServer': isDevServer(),
  }

  return template_values


class MainPage(webapp2.RequestHandler):
  def get(self, urlLocale=None):
    userLocale = getLocale(urlLocale, self.request.headers.get('accept_language'))
    template_values = getCommonTemplateValues(self, urlLocale, userLocale)
    template_values['isIncludeAbout'] = True
    template_values['pageHtml'] = getAllLocalesTranslationsHtml(
                                    urlLocale, userLocale)
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class CanonPage(webapp2.RequestHandler):
  def get(self, paliTextPath, urlLocale=None):
    userLocale = getLocale(urlLocale, self.request.headers.get('accept_language'))
    result = checkPath(self.request.path, urlLocale, paliTextPath, userLocale)
    if not result['isValid']:
      self.abort(404)
    template_values = getCommonTemplateValues(self, urlLocale, userLocale)
    template_values['pageHtml'] = result['pageHtml']
    template_values['htmlTitle'] = result['htmlTitle']
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class TranslationPage(webapp2.RequestHandler):
  def get(self, paliTextPath, translationLocale, translator, urlLocale=None):
    userLocale = getLocale(urlLocale, self.request.headers.get('accept_language'))
    result = checkPath(self.request.path, urlLocale, paliTextPath, userLocale, translationLocale, translator)
    if not result['isValid']:
      self.abort(404)
    template_values = getCommonTemplateValues(self, urlLocale, userLocale)
    template_values['pageHtml'] = result['pageHtml']
    template_values['htmlTitle'] = result['htmlTitle']
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class ContrastReadingPage(webapp2.RequestHandler):
  def get(self, paliTextPath, translationLocale, translator, urlLocale=None):
    userLocale = getLocale(urlLocale, self.request.headers.get('accept_language'))
    result = checkPath(self.request.path, urlLocale, paliTextPath, userLocale, translationLocale, translator)
    if not result['isValid']:
      self.abort(404)
    template_values = getCommonTemplateValues(self, urlLocale, userLocale)
    template_values['pageHtml'] = result['pageHtml']
    template_values['htmlTitle'] = result['htmlTitle']
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([
  PathPrefixRoute(r'/<urlLocale:en_US|zh_TW|zh_CN|fr_FR|vi_VN>', [
    webapp2.Route(r'/', handler=MainPage),
    webapp2.Route(r'<paliTextPath:/.+>/<translationLocale:en_US|zh_TW|zh_CN|fr_FR|vi_VN>/<translator>/ContrastReading', handler=ContrastReadingPage),
    webapp2.Route(r'<paliTextPath:/.+>/<translationLocale:en_US|zh_TW|zh_CN|fr_FR|vi_VN>/<translator>', handler=TranslationPage),
    webapp2.Route(r'<paliTextPath:/.+>', handler=CanonPage)
  ]),
  webapp2.Route(r'/', handler=MainPage),
  webapp2.Route(r'<paliTextPath:^/.+>/<translationLocale:en_US|zh_TW|zh_CN|fr_FR|vi_VN>/<translator>/ContrastReading', handler=ContrastReadingPage),
  webapp2.Route(r'<paliTextPath:^/.+>/<translationLocale:en_US|zh_TW|zh_CN|fr_FR|vi_VN>/<translator>', handler=TranslationPage),
  webapp2.Route(r'<paliTextPath:^/.+>', handler=CanonPage)],
  debug=True)
