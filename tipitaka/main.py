#!/usr/bin/env python
# -*- coding:utf-8 -*-

import webapp2, jinja2, os, sys, json

sys.path.append(os.path.join(os.path.dirname(__file__), 'gaelibs'))
from url import getHtmlTitle, isValidCanonPath, getCanonPageHtml, isValidTranslationOrContrastReadingPage, getTranslationPageHtml, getContrastReadingPageHtml

sys.path.append(os.path.join(os.path.dirname(__file__), 'common/gae/libs'))
from localeUtil import getLocale, parseAcceptLanguage
from misc import isCompiledJS, isTrack

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
    'htmlTitle': u'',
    'userLocale': userLocale,
    'langQs': json.dumps(parseAcceptLanguage(self.request.headers.get('accept_language'))),
    'urlLocale': urlLocale,
    'isCompiledJS': isCompiledJS(self),
    'isTrack': isTrack(self),
    'urlpath': self.request.path,
    'reqHandlerName': self.__class__.__name__
  }

  return template_values


class MainPage(webapp2.RequestHandler):
  def get(self, urlLocale=None):
    template_values = getCommonTemplateValues(self, urlLocale)
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class CanonPage(webapp2.RequestHandler):
  def get(self, urlLocale=None, path1=None, path2=None, path3=None, path4=None, path5=None):
    result = isValidCanonPath(path1, path2, path3, path4, path5)
    if not result['isValid']:
      self.abort(404)
    template_values = getCommonTemplateValues(self, urlLocale)
    template_values['canonPageHtml'] = getCanonPageHtml(result['node'], self.request.path, i18n)
    template_values['htmlTitle'] = getHtmlTitle(urlLocale, result['texts'], i18n)
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class TranslationPage(webapp2.RequestHandler):
  def get(self, path1, path2, path3, locale, translator, urlLocale=None, path4=None, path5=None):
    result = isValidTranslationOrContrastReadingPage(path1, path2, path3, path4, path5, locale, translator)
    if not result['isValid']:
      self.abort(404)
    template_values = getCommonTemplateValues(self, urlLocale)
    template_values['translationPageHtml'] = getTranslationPageHtml(locale, translator, result['node'], self.request.path, i18n)
    template_values['htmlTitle'] = getHtmlTitle(urlLocale, result['texts'], i18n)
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class ContrastReadingPage(webapp2.RequestHandler):
  def get(self, path1, path2, path3, locale, translator, urlLocale=None, path4=None, path5=None):
    result = isValidTranslationOrContrastReadingPage(path1, path2, path3, path4, path5, locale, translator)
    if not result['isValid']:
      self.abort(404)
    template_values = getCommonTemplateValues(self, urlLocale)
    template_values['contrastReadingPageHtml'] = getContrastReadingPageHtml(locale, translator, result['node'], self.request.path, i18n)
    template_values['htmlTitle'] = getHtmlTitle(urlLocale, result['texts'], i18n)
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/canon/<path1>/<path2>/<path3>/<path4>/<path5>/<locale:en_US|zh_TW|zh_CN>/<translator>/ContrastReading', handler=ContrastReadingPage),
  webapp2.Route(r'/canon/<path1>/<path2>/<path3>/<path4>/<path5>/<locale:en_US|zh_TW|zh_CN>/<translator>/ContrastReading', handler=ContrastReadingPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/canon/<path1>/<path2>/<path3>/<path4>/<path5>/<locale:en_US|zh_TW|zh_CN>/<translator>', handler=TranslationPage),
  webapp2.Route(r'/canon/<path1>/<path2>/<path3>/<path4>/<path5>/<locale:en_US|zh_TW|zh_CN>/<translator>', handler=TranslationPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/canon/<path1>/<path2>/<path3>/<path4>/<path5>', handler=CanonPage),
  webapp2.Route(r'/canon/<path1>/<path2>/<path3>/<path4>/<path5>', handler=CanonPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/canon/<path1>/<path2>/<path3>/<path4>/<locale:en_US|zh_TW|zh_CN>/<translator>/ContrastReading', handler=ContrastReadingPage),
  webapp2.Route(r'/canon/<path1>/<path2>/<path3>/<path4>/<locale:en_US|zh_TW|zh_CN>/<translator>/ContrastReading', handler=ContrastReadingPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/canon/<path1>/<path2>/<path3>/<path4>/<locale:en_US|zh_TW|zh_CN>/<translator>', handler=TranslationPage),
  webapp2.Route(r'/canon/<path1>/<path2>/<path3>/<path4>/<locale:en_US|zh_TW|zh_CN>/<translator>', handler=TranslationPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/canon/<path1>/<path2>/<path3>/<path4>', handler=CanonPage),
  webapp2.Route(r'/canon/<path1>/<path2>/<path3>/<path4>', handler=CanonPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/canon/<path1>/<path2>/<path3>/<locale:en_US|zh_TW|zh_CN>/<translator>/ContrastReading', handler=ContrastReadingPage),
  webapp2.Route(r'/canon/<path1>/<path2>/<path3>/<locale:en_US|zh_TW|zh_CN>/<translator>/ContrastReading', handler=ContrastReadingPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/canon/<path1>/<path2>/<path3>/<locale:en_US|zh_TW|zh_CN>/<translator>', handler=TranslationPage),
  webapp2.Route(r'/canon/<path1>/<path2>/<path3>/<locale:en_US|zh_TW|zh_CN>/<translator>', handler=TranslationPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/canon/<path1>/<path2>/<path3>', handler=CanonPage),
  webapp2.Route(r'/canon/<path1>/<path2>/<path3>', handler=CanonPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/canon/<path1>/<path2>', handler=CanonPage),
  webapp2.Route(r'/canon/<path1>/<path2>', handler=CanonPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/canon/<path1>', handler=CanonPage),
  webapp2.Route(r'/canon/<path1>', handler=CanonPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/canon', handler=CanonPage),
  webapp2.Route(r'/canon', handler=CanonPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/', handler=MainPage),
  webapp2.Route(r'/', handler=MainPage)],
  debug=True)
