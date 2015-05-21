#!/usr/bin/env python
#
# Description: Python script to convert SQL Developer export xml data to
# DBUnit dataset xml format.
#
# Author: Marcelo Santos Guimaraes
# Email: marcsgbh@gmail.com
# Last Modified: May 21 2015
# Version: 0.1
#

import lxml.etree as ET
import sys, getopt, re, datetime
import os.path

def usage():
  print 'Usage: '+sys.argv[0]+' -i input [-t table] [-o output] [-x xslt] [-l]'

def note():
  print "Note: libxml2 and lxml are required. They can be installed using:"
  print "      brew install libxml2"
  print "      sudo pip install lxml"

def main(argv):
  xsltFile = "sql.xslt"
  outputFile = ''
  tableName = ''
  inputFile = ''

  # translate element/attribute names to lower case?
  lower = False

  # Handle input
  try:
    opts, args = getopt.getopt(argv, "lhi:o:t:x:",["input=","output="])
  except getopt.GetoptError:
    usage()
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      note()
      exit(2)
    elif opt in ("-i", "--input"):
      inputFile = arg
    elif opt in ("-o", "--output"):
      outputFile = arg
    elif opt in ("-t", "--table"):
      tableName = arg
    elif opt in ("-x", "--xslt"):
      xsltFile = arg
    elif opt == "-l":
      lower = True
      print "info: avoid conversion to lower case for large XML files."

  if not inputFile:
    print "error: input not provided."
    usage()
    exit(2)
  elif not os.path.isfile(inputFile):
    print "error: input file " + inputFile + " not found."
    exit(2)

  if not tableName:
    print "info: default table name is 'TABLE'"
    tableName = "TABLE"

  if not outputFile:
    print "info: default output file is 'output.xml'"
    outputFile = "output.xml"

  if not os.path.isfile(xsltFile):
    print "error: xslt file " + xsltFile + " not found."
    exit(2)

  print

  # Parse xslt file and set table name variable
  xslt = ET.parse(xsltFile)
  namespaces = {'xsl': 'http://www.w3.org/1999/XSL/Transform'}
  tableVars = xslt.findall('xsl:variable', namespaces)
  tableVars[0].text = tableName

  # Parse input and transform XML
  transform = ET.XSLT(xslt)
  dom = ET.parse(inputFile)
  newdom = transform(dom)

  for element in newdom.findall(tableName):
    if lower:
      element.tag = element.tag.lower()
    for attr in element.attrib:
      if lower:
        name = attr.lower()
      else:
        name = attr
      value = element.get(attr)
      # Check if attribute value is a date. If it is, convert to ISO format
      matchValue = re.match('^\d\d/\d\d/\d\d \d\d:\d\d:\d\d', value)
      if matchValue:
        value = formatFullDate(matchValue.group())
      else:
        matchValue = re.match('^\d\d/\d\d/\d\d$', value)
        if matchValue:
          value = formatSimpleDate(matchValue.group())
        else:
          matchValue = re.match('^\d*,\d*$', value)
          if matchValue:
            value = formatDoubleValue(matchValue.group())

      del element.attrib[attr] # delete old uppercase attribute

      # only add atribute if value is not empty
      if value:
        element.set(name, value) # create new lowercase attribute

  # Save output file
  print "'"+outputFile+"' saved."
  newdom.write(outputFile)

# Convert date from sql output format to ISO format
def formatFullDate(date):
  newDate = datetime.datetime.strptime(date, '%d/%m/%y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
  return newDate

def formatSimpleDate(date):
  newDate = datetime.datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d')
  return newDate

# Replace comma ',' by dot '.' in dollar values
def formatDoubleValue(value):
  newValue = value.replace(',','.')
  return newValue

if __name__ == "__main__":
   main(sys.argv[1:])
