#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import time

# http://www.yattag.org/
from yattag import Doc

INDEX = "index.html"
RFC3339DATE = "%Y-%m-%d"

def formatdate(str):
    bdate = time.strptime(str, RFC3339DATE)
    return time.strftime("Pouètes du %d %B %Y", bdate)

doc, tag, text = Doc().tagtext()
doc.asis('<?xml version="1.0" ?>\n')
doc.asis('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"')

with tag('html', ('xml:lang', 'fr'), lang = 'fr', xmlns = 'http://www.w3.org/1999/xhtml'):
    with tag('head'):
        with tag('title'):
            text("Mercredi Fiction")
    text('\n')
    epubs = {}
    with tag('body'):
        with tag('h1'):
            text("Mercredi Fiction")
        text('\n')
        for file in os.listdir('.'):
               result = re.search("-([0-9-]+)\.epub", file)
               if result:                
                  epubs[result.group(1)] = file
        with tag('ul'):
            text('\n')
            for date in sorted(epubs, reverse=True):
                with tag('li'):
                    with tag('a', href = epubs[date]):
                        text(formatdate(date))
                text('\n')
            text('\n')
text('\n')
outfile = open(INDEX, 'w')
outfile.write(doc.getvalue())
outfile.close()

