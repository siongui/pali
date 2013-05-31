#!/usr/bin/env python
# -*- coding:utf-8 -*-

# References:
# http://code.activestate.com/recipes/510399-byte-to-hex-and-hex-to-byte-string-conversion/
# http://stackoverflow.com/questions/606191/convert-byte-array-to-python-string

# some utf8 characters conflict with the format of XML, which causes error while parsing XML
# so utf8 chars are stored in hex string, which needed to be decoded before being used.

def HexStringToString(hexString):
  # convert hex string to utf8 string
  # example: "%2c%e3%80" -> "\x2C\xE3\x80"
  bytes = []
  hexStr = ''.join( hexString.split("%") )
  for i in range(0, len(hexStr), 2):
    bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

  # decode as utf8
  try:
    string = ''.join( bytes ).decode("utf-8")
  except UnicodeDecodeError:
    string = u"Sorry! Something wrong with the database. We cannot get explain of this word in this dictionary."

  return string

def StringToHexString(string):
  # convert string to hex string
  string = string.encode('utf8')
  return ''.join( [ "%02X " % ord( x ) for x in string ] ).strip().replace(' ','%')

if __name__ == '__main__':
  # for test purpose
  testStr = "%2c%e3%80%90%e5%bd%a2%e3%80%91%e6%97%a0%e7%a2%8d%e7%9a%84%e3%80%82"
  print("Test Hex String:      %s" % testStr)
  string = HexStringToString(testStr)
  print("Converted String:     %s" % string)
  hexstr = StringToHexString(string)
  print("Converted Hex String: %s" % hexstr)
  string = HexStringToString(hexstr)
  print("Converted String:     %s" % string)
