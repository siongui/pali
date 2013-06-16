#!/usr/bin/env python
# -*- coding:utf-8 -*-

from i18n import locales

def getLocale(urlLocale, acptLang):
  if urlLocale in locales:
    return urlLocale
  else:
    return determineLocale(acptLang)


def parseAcceptLanguage(value):
  # array of (language, q) pairs
  pairs = []

  try:
    langQs = value.split(',')
  except:
    return pairs
  for langQ in langQs:
    if ';' in langQ:
      locale, q = langQ.split(';', 1)
      if '=' in q:
        q = q.split('=', 1)[1]
      pairs.append([locale.strip(), q.strip()])
    else:
      pairs.append([langQ.strip(), '1'])

  return pairs


def determineLocale(value):
  try:
    pairs = parseAcceptLanguage(value)

    for pair in pairs:
      lang = pair[0].lower()
      if lang == 'zh-tw':
        return 'zh_TW'
      if lang == 'zh-hk':
        return 'zh_TW'
      if lang == 'zh-cn':
        return 'zh_CN'
      if lang.startswith('zh'):
        return 'zh_CN'
      if lang.startswith('en'):
        return 'en_US'
      if lang.startswith('fr'):
        return 'fr_FR'
      if lang.startswith('vi'):
        return 'vi_VN'

  except:
    return 'en_US'

  return 'en_US'


if __name__ == '__main__':
  # for test purpose
  print('da, en-gb;q=0.8, en;q=0.7')
  print(parseAcceptLanguage('da, en-gb;q=0.8, en;q=0.7'))
  print(determineLocale('da, en-gb;q=0.8, en;q=0.7'))
  print('es-mx,es,en')
  print(parseAcceptLanguage('es-mx,es,en'))
  print(determineLocale('es-mx,es,en'))
  print('en-us,en;q=0.5')
  print(parseAcceptLanguage('en-us,en;q=0.5'))
  print(determineLocale('en-us,en;q=0.5'))
  print('tr-tr,tr;q=0.8,en-us;q=0.5,en;q=0.3')
  print(parseAcceptLanguage('tr-tr,tr;q=0.8,en-us;q=0.5,en;q=0.3'))
  print(determineLocale('tr-tr,tr;q=0.8,en-us;q=0.5,en;q=0.3'))
  print('en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4')
  print(parseAcceptLanguage('en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4'))
  print(determineLocale('en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4'))
  print('zh-hk,zh;q=0.8,zh-tw;q=0.7,zh-cn;q=0.5,en-us;q=0.3,en;q=0.2')
  print(parseAcceptLanguage('zh-hk,zh;q=0.8,zh-tw;q=0.7,zh-cn;q=0.5,en-us;q=0.3,en;q=0.2'))
  print(determineLocale('zh-hk,zh;q=0.8,zh-tw;q=0.7,zh-cn;q=0.5,en-us;q=0.3,en;q=0.2'))
  print('zh,en;q=0.9')
  print(parseAcceptLanguage('zh,en;q=0.9'))
  print(determineLocale('zh,en;q=0.9'))

  print(parseAcceptLanguage(None))
  print(determineLocale(None))
  print(parseAcceptLanguage(312))
  print(determineLocale(312))
