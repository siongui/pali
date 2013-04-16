#!/usr/bin/env python
# -*- coding:utf-8 -*-

import webapp2, jinja2, os, sys, json, urllib2

sys.path.append(os.path.join(os.path.dirname(__file__), 'gaelibs'))
from url import isValidPrefixAndWord, getPrefixHtml, getWordHtml, getHtmlTitle

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


def getCommonTemplateValues(self, urlLocale, prefix=None, word=None):
  userLocale = getLocale(urlLocale, self.request.headers.get('accept_language'))
  i18n.get_i18n().set_locale(userLocale)
  template_values = {
    'htmlTitle': getHtmlTitle(userLocale, self.__class__.__name__, i18n, prefix, word),
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


class WordPage(webapp2.RequestHandler):
  def get(self, prefix, word, urlLocale=None):
    if not isValidPrefixAndWord(prefix, word):
      self.abort(404)
    template_values = getCommonTemplateValues(self, urlLocale, prefix, word)
    wordHtml = getWordHtml(prefix, word, urlLocale)
    if wordHtml is None:
      self.abort(404)
    template_values['wordHtml'] = wordHtml
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class PrefixPage(webapp2.RequestHandler):
  def get(self, prefix,  urlLocale=None):
    if not isValidPrefixAndWord(prefix, None):
      self.abort(404)
    template_values = getCommonTemplateValues(self, urlLocale, prefix)
    prefixHtml = getPrefixHtml(prefix, urlLocale)
    if prefixHtml is None:
      self.abort(404)
    template_values['prefixHtml'] = prefixHtml
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class RedirectPage(webapp2.RequestHandler):
  def get(self):
    self.redirect('/')


class JsonPage(webapp2.RequestHandler):
  def get(self, partialPathi=None):
    url = 'http://%s.palidictionary.appspot.com/%s' % (self.request.get('v'), self.request.path)
    result = urllib2.urlopen(url)
    self.response.out.write(result.read())


app = webapp2.WSGIApplication([
  webapp2.Route(r'/browse/noSuchWord', handler=RedirectPage),
  webapp2.Route(r'/', handler=MainPage),
  webapp2.Route(r'/about', handler=MainPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/', handler=MainPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/browse/<prefix:.+>/<word:.+>', handler=WordPage),
  webapp2.Route(r'/browse/<prefix:.+>/<word:.+>', handler=WordPage),
  webapp2.Route(r'/<urlLocale:en_US|zh_TW|zh_CN>/browse/<prefix:.+>', handler=PrefixPage),
  webapp2.Route(r'/browse/<prefix:.+>', handler=PrefixPage),
  webapp2.Route(r'/json/<:.*>', handler=JsonPage)],
  debug=True)
