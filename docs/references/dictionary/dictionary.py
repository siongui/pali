#!/usr/bin/env python
# -*- coding:utf-8 -*-

import xml.dom.minidom
from google.appengine.ext import ndb
from convertstr import HexStringToString


def decodeItem(item):
  dict = item.getElementsByTagName("dict")[0]
  word = item.getElementsByTagName("word")[0]
  explain = item.getElementsByTagName("explain")[0]

  dictstr = dict.childNodes[0].data
  wordstr = word.childNodes[0].data
  explainstr = HexStringToString(explain.childNodes[0].data)

  return dictstr, wordstr, explainstr


def getHTMLTableCode(dictstr, wordstr, explainstr):
  return u"""<table border="1" bordercolor="#00FFFF" style="background-color:#CCFFFF" width="%s" cellpadding="5" cellspacing="0">
         <tr><th>字典</th><td>%s</td></tr>
         <tr><th>單字</th><td>%s</td></tr>
         <tr><th>解釋</th><td>%s</td></tr></table>""" % (u'100%', dictstr, wordstr, explainstr)


def decodeXML(xmlfilename, xmlfile):
  # input: xml file of pali word definition
  dom = xml.dom.minidom.parseString(xmlfile)

  items = dom.getElementsByTagName("item")
  HTMLstr = """<table width="%s" style="border:10px solid #98FB98;
               -webkit-border-radius:13px;-moz-border-radius:13px;border-radius:13px;">
                 <th>%s (%s)</th>""" % (u'100%', unicode(xmlfilename)[0:-4], unicode(xmlfilename))
  for item in items:
    HTMLstr += u'<tr><td>'
    dictstr, wordstr, explainstr = decodeItem(item)
    HTMLstr += getHTMLTableCode(dictstr, wordstr, explainstr)
    HTMLstr += u'</td></tr>'

  HTMLstr += u'</table>'
  HTMLstr += u'</br>'

  return HTMLstr


class PaliWord(ndb.Model):
  xmlfilename = ndb.StringProperty()
  xmlfiledata = ndb.TextProperty()


def storeToNDB(filename, filedata):
  # id = filename without .xml extension
  paliword = PaliWord(id = filename[0:-4],
                      xmlfilename = filename,
                      xmlfiledata = filedata)
  paliword.put()
  return '%s : ok' % filename


def lookup(word):
  paliword = PaliWord.get_by_id(word)
  if (paliword):
    return decodeXML(paliword.xmlfilename, paliword.xmlfiledata.encode('utf8'))
  else:
    return u'查無此字(No Such Word)'


def jsonpDecodeXML(xmlfilename, xmlfile):
  # input: xml file of pali word definition
  dom = xml.dom.minidom.parseString(xmlfile)

  items = dom.getElementsByTagName("item")
  result = []
  for item in items:
    dictstr, wordstr, explainstr = decodeItem(item)
    result.append((dictstr, wordstr, explainstr))

  # return valus is "list of 3-tuples"
  return result


def jsonpLookup(word):
  jsonData = {}
  jsonData['word'] = word
  if word == '':
    jsonData['data'] = None
    return jsonData

  paliword = PaliWord.get_by_id(word)
  if (paliword):
    jsonData['data'] = jsonpDecodeXML(paliword.xmlfilename, paliword.xmlfiledata.encode('utf8'))
    return jsonData
  else:
    jsonData['data'] = None
    return jsonData
