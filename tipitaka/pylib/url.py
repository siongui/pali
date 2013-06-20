#!/usr/bin/env python
# -*- coding:utf-8 -*-

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


def serveCanonPageHtml(reqPath, urlLocale, paliTextPath, userLocale):
  result = isValidPath(paliTextPath)
  if result['isValid']:
    data = { 'title': getHtmlTitle(urlLocale, result['texts'], userLocale),
             'html': getCanonPageHtml(result['node'], reqPath, userLocale) }
    return data


def serveTranslationPageHtml(reqPath, urlLocale, paliTextPath, userLocale,
                             translationLocale, translator):
  result = isValidPath(paliTextPath, translationLocale, translator)
  if result['isValid']:
    data = { 'title': getHtmlTitle(urlLocale, result['texts'], userLocale,
                                   translator, False),
             'html': getTranslationPageHtml(translationLocale, translator,
                         result['node']['action'], reqPath, userLocale) }
    return data


def serveContrastReadingPageHtml(reqPath, urlLocale, paliTextPath, userLocale,
                                 translationLocale, translator):
  result = isValidPath(paliTextPath, translationLocale, translator)
  if result['isValid']:
    data = { 'title': getHtmlTitle(urlLocale, result['texts'], userLocale,
                                   translator, False),
             'html': getContrastReadingPageHtml(translationLocale, translator,
                         result['node']['action'], reqPath, userLocale) }
    return data


if __name__ == '__main__':
  # for test purpose
  pass
