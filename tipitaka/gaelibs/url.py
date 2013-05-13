#!/usr/bin/env python
# -*- coding:utf-8 -*-

from translationInfo import getAllLocalesTranslationsTemplateValues
from template import getJinja2Env
from pathInfo import isValidPath
from htmlTitle import getHtmlTitle
from processHtml import getCanonPageHtml
from processHtml import getTranslationPageHtml
from processHtml import getContrastReadingPageHtml


def checkPath(reqPath, urlLocale, paliTextPath, userLocale,
              translationLocale=None, translator=None):
  result = isValidPath(paliTextPath, translationLocale, translator)
  if result['isValid']:
    # this is a valid path
    if translationLocale:
      if reqPath.endswith('ContrastReading'):
        # contrast reading page
        result['htmlTitle'] = getHtmlTitle(urlLocale, result['texts'],
                                userLocale, translator, True)
        result['pageHtml'] = getContrastReadingPageHtml(translationLocale,
          translator, result['node']['action'], reqPath, userLocale)
      else:
        # translation page
        result['htmlTitle'] = getHtmlTitle(urlLocale, result['texts'],
                                userLocale, translator, False)
        result['pageHtml'] = getTranslationPageHtml(translationLocale,
          translator, result['node']['action'], reqPath, userLocale)
    else:
      # canon page
      result['htmlTitle'] = getHtmlTitle(urlLocale, result['texts'], userLocale)
      result['pageHtml'] = getCanonPageHtml(result['node'], reqPath, userLocale)

  return result


def getAllLocalesTranslationsHtml(urlLocale, userLocale):
  template = getJinja2Env(userLocale).get_template('info.html')
  return template.render({'urlLocale': urlLocale,
                          'userLocale': userLocale,
                          'localeTranslations': getAllLocalesTranslationsTemplateValues()})


if __name__ == '__main__':
  # for test purpose
  pass
