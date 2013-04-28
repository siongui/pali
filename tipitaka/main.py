#!/usr/bin/env python
# -*- coding:utf-8 -*-

import webapp2, jinja2, os, sys, json, urllib2
from  webapp2_extras.routes import PathPrefixRoute

sys.path.append(os.path.join(os.path.dirname(__file__), 'gaelibs'))
from url import getCanonPageHtml, getTranslationPageHtml, getContrastReadingPageHtml, getAllLocalesTranslationsHtml
from htmlTitle import getHtmlTitle
from pathInfo import isValidPath

sys.path.append(os.path.join(os.path.dirname(__file__), 'common/gae/libs'))
from localeUtil import getLocale, parseAcceptLanguage
from misc import isCompiledJS, isTrack

# zipimport babel and gaepytz
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'common/gae/libs/babel.zip'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'common/gae/libs/pytz.zip'))

from webapp2_extras import i18n

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader([os.path.join(os.path.dirname(__file__), 'app'),
                                    os.path.join(os.path.dirname(__file__), 'app/css'),
                                    os.path.join(os.path.dirname(__file__), 'app/partials')]),
    extensions=['jinja2.ext.i18n'],
    variable_start_string='{$',
    variable_end_string='$}')

jinja_environment.install_gettext_translations(i18n)


def getCommonTemplateValues(self, urlLocale):
  userLocale = getLocale(urlLocale, self.request.headers.get('accept_language'))
  i18n.get_i18n().set_locale(userLocale)
  template_values = {
    'htmlTitle': u'',
    'userLocale': userLocale,
    'langQs': json.dumps(parseAcceptLanguage(self.request.headers.get('accept_language'))),
    'urlLocale': urlLocale,
    'isCompiledJS': isCompiledJS(self),
    'isTrack': isTrack(self),
    'reqHandlerName': self.__class__.__name__
  }

  return template_values


class MainPage(webapp2.RequestHandler):
  def get(self, urlLocale=None):
    template_values = getCommonTemplateValues(self, urlLocale)
    template_values['allLocalesTranslationsHtml'] = getAllLocalesTranslationsHtml(urlLocale)
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class CanonPage(webapp2.RequestHandler):
  def get(self, paliTextPath, urlLocale=None):
    result = isValidPath(paliTextPath)
    if not result['isValid']:
      self.abort(404)
    template_values = getCommonTemplateValues(self, urlLocale)
    template_values['canonPageHtml'] = getCanonPageHtml(result['node'], self.request.path, i18n)
    template_values['htmlTitle'] = getHtmlTitle(urlLocale, result['texts'])
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class TranslationPage(webapp2.RequestHandler):
  def get(self, paliTextPath, translationLocale, translator, urlLocale=None):
    result = isValidPath(paliTextPath, translationLocale, translator)
    if not result['isValid']:
      self.abort(404)
    template_values = getCommonTemplateValues(self, urlLocale)
    template_values['translationPageHtml'] = getTranslationPageHtml(translationLocale, translator, result['node'], self.request.path, i18n)
    template_values['htmlTitle'] = getHtmlTitle(urlLocale, result['texts'], translator, False, i18n)
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class ContrastReadingPage(webapp2.RequestHandler):
  def get(self, paliTextPath, translationLocale, translator, urlLocale=None):
    result = isValidPath(paliTextPath, translationLocale, translator)
    if not result['isValid']:
      self.abort(404)
    template_values = getCommonTemplateValues(self, urlLocale)
    template_values['contrastReadingPageHtml'] = getContrastReadingPageHtml(translationLocale, translator, result['node'], self.request.path, i18n)
    template_values['htmlTitle'] = getHtmlTitle(urlLocale, result['texts'], translator, True, i18n)
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class JsonPage(webapp2.RequestHandler):
  def get(self):
    url = 'http://%s.palidictionary.appspot.com/%s' % (self.request.get('v'), self.request.path)
    result = urllib2.urlopen(url)
    self.response.out.write(result.read())


app = webapp2.WSGIApplication([
  (r'/json/.+', JsonPage),
  PathPrefixRoute(r'/<urlLocale:en_US|zh_TW|zh_CN>', [
    webapp2.Route(r'/', handler=MainPage),
    webapp2.Route(r'<paliTextPath:/.+>/<translationLocale:en_US|zh_TW|zh_CN>/<translator>/ContrastReading', handler=ContrastReadingPage),
    webapp2.Route(r'<paliTextPath:/.+>/<translationLocale:en_US|zh_TW|zh_CN>/<translator>', handler=TranslationPage),
    webapp2.Route(r'<paliTextPath:/.+>', handler=CanonPage)
  ]),
  webapp2.Route(r'/', handler=MainPage),
  webapp2.Route(r'<paliTextPath:^/.+>/<translationLocale:en_US|zh_TW|zh_CN>/<translator>/ContrastReading', handler=ContrastReadingPage),
  webapp2.Route(r'<paliTextPath:^/.+>/<translationLocale:en_US|zh_TW|zh_CN>/<translator>', handler=TranslationPage),
  webapp2.Route(r'<paliTextPath:^/.+>', handler=CanonPage)],
  debug=True)
