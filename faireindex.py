#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import time
import locale

# http://www.yattag.org/
from yattag import Doc

INDEX = "index.html"
LAST = "mercredifiction-dernier.epub"
RFC3339DATE = "%Y-%m-%d"

def formatdate(str):
    bdate = time.strptime(str, RFC3339DATE)
    return time.strftime("%d %B %Y", bdate)

locale.setlocale(locale.LC_TIME, 'fr_FR')
  
doc, tag, text = Doc().tagtext()
doc.asis('<?xml version="1.0" ?>\n')
doc.asis('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"')

with tag('html', ('xml:lang', 'fr'), lang = 'fr', xmlns = 'http://www.w3.org/1999/xhtml'):
    with tag('head'):
        with tag('title'):
            text("Mercredi Fiction")
        with tag('meta', ('http-equiv', "Content-Type"), content = "text/html; charset=UTF-8"):
            pass
    text('\n')
    epubs = {}
    with tag('body'):
        for file in os.listdir('.'):
               result = re.search("-([0-9-]+)\.epub", file)
               if result:                
                  epubs[result.group(1)] = file
        sorteddates = sorted(epubs, reverse=True)
        with tag('h1'):
            text("Mercredi Fiction")    
        text('\n')
        if os.path.exists(LAST):
            os.remove(LAST)
        os.symlink(epubs[sorteddates[0]], LAST)
        with tag('p'):
            with tag('a', href = LAST):
                text("Dernière version")
            text(" (le %s)" % formatdate(sorteddates[0]))
        text('\n')
        with tag('p'):
            text("Versions précédentes")
            with tag('ul'):
                text('\n')
                for date in sorteddates[1:]:
                    with tag('li'):
                        with tag('a', href = epubs[date]):
                            text("Pouètes du %s" % formatdate(date))
                    text('\n')
                text('\n')
        with tag('br'):
            pass
        with tag('p'):
            text("Code disponible ")
            with tag('a', href = "https://github.com/bortzmeyer/MercrediFiction"):
                text("sur Github")
text('\n')
outfile = open(INDEX, 'w')
outfile.write(doc.getvalue())
outfile.close()

