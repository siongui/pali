#!/usr/bin/env python
# -*- coding:utf-8 -*-

def getUserLocale(qryLocale, acptLang):
  locale = qryLocale
  if (locale):
    if locale not in ['en_US', 'zh_TW', 'zh_CN']:
      locale = 'en_US'
  else:
    # no locale set in URL query
    accept_languages = acptLang
    if accept_languages is None:
      locale = 'en_US'
    else:
      languages = accept_languages.split(",")
      language_q_pairs = []
      for language in languages:
        if language.split(";")[0] == language:
          language_q_pairs.append((language, "1"))
        else:
          locale = language.split(";")[0]
          q = language.split(";")[1].split("=")[1]
          language_q_pairs.append((locale, q))
      #self.response.out.write(language_q_pairs)
      if (language_q_pairs[0][0].lower() == 'zh-tw'):
        locale = 'zh_TW'
      elif (language_q_pairs[0][0].lower() == 'zh-hk'):
        locale = 'zh_TW'
      elif (language_q_pairs[0][0].lower() == 'zh-cn'):
        locale = 'zh_CN'
      elif (language_q_pairs[0][0].lower().startswith('zh')):
        locale = 'zh_CN'
      else:
        locale = 'en_US'
  #self.response.out.write("locale: %s" % locale)
  return locale


if __name__ == '__main__':
  # for test purpose
  print(getUserLocale(None, None))
