#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib

def get_bp():
    class myContentHandler(ContentHandler):

        def __init__ (self):
            self.inItem = False
            self.inContent = False
            self.theContent = ""
            self.salida = "<h1>Noticias de Barrapunto</h1><br><br>"

        def startElement (self, name, attrs):
            if name == 'item':
                self.inItem = True
            elif self.inItem:
                if name == 'title':
                    self.inContent = True
                elif name == 'link':
                    self.inContent = True
                elif name == 'description':
                    self.inContent = True
                
        def endElement (self, name):
            if name == 'item':
                self.inItem = False
            elif self.inItem:
                if name == 'title':
                    line = "<li><strong>Title: " + self.theContent + "</strong>."
                    # To avoid Unicode trouble
                    self.salida += line
                    self.inContent = False
                    self.theContent = ""
                elif name == 'link':
                    self.salida += "Link: <a href='" + self.theContent + "'>" + self.theContent + "</a>.<br>"
                    self.inContent = False
                    self.theContent = ""
                elif name == 'description':
                    self.salida += "Descripcion: " + self.theContent + ".<br><br>"
                    self.inContent = False
                    self.theContent = ""    
                
        def characters (self, chars):
            if self.inContent:
                self.theContent = self.theContent + chars
                
    # --- Main prog
        
    # Load parser and driver

    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    # Ready, set, go!

    f = urllib.urlopen("http://barrapunto.com/index.rss")

    theParser.parse(f)
    
    return theHandler.salida


