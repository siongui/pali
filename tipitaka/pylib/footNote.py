#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lxml import etree

def processNotes(elm):
  # http://infohost.nmt.edu/tcc/help/pubs/pylxml/web/index.html
  # http://effbot.org/zone/element-xpath.htm
  notes = elm.xpath(".//span[@class='note']")

  body = elm.find('body')

  for index, note in enumerate(notes):
    # http://stackoverflow.com/questions/7981840/how-to-remove-an-element-in-lxml
    # http://stackoverflow.com/questions/1812764/replacing-elements-with-lxml-html
    fidx = index + 1
    fn = etree.fromstring('<a name="fnt-%d" href="#fn-%d"><sup>[%d]</sup></a>'
        % (fidx, fidx, fidx) )
    fn.tail = note.tail
    fn.tag = 'span'
    note.getparent().replace(note, fn)

    div = etree.fromstring('<div><a name="fn-%d" href="#fnt-%d">%d</a>. </div>'
        % (fidx, fidx, fidx) )
    div[0].tag = 'span'

    note.tail = None
    note.text = note.text[1:-1]
    div.append(note)
    body.append(div)


def processTranslatedPElementsNotes(trPElms):
  notes = []
  for trPElm in trPElms:
    notes += trPElm.xpath(".//span[@class='note']")

  footNotes = etree.fromstring('<div></div>')
  for index, note in enumerate(notes):
    fidx = index + 1
    fn = etree.fromstring('<a name="fnt-%d" href="#fn-%d"><sup>[%d]</sup></a>'
        % (fidx, fidx, fidx) )
    fn.tail = note.tail
    fn.tag = 'span'
    note.getparent().replace(note, fn)

    div = etree.fromstring('<div><a name="fn-%d" href="#fnt-%d">%d</a>. </div>'
        % (fidx, fidx, fidx) )
    div[0].tag = 'span'

    note.tail = None
    note.text = note.text[1:-1]
    div.append(note)
    footNotes.append(div)

  return footNotes
