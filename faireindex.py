#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import time
import locale

# http://www.yattag.org/
from yattag import Doc

INDEX = "index.html"
LASTEPUB = "mercredifiction-dernier.epub"
LASTHTML = "mercredifiction-dernier.html"
RFC3339DATE = "%Y-%m-%d"

def formatdate(str):
    bdate = time.strptime(str, RFC3339DATE)
    return time.strftime("%d %B %Y", bdate)

locale.setlocale(locale.LC_TIME, 'fr_FR')
  
doc, tag, text = Doc().tagtext()
doc.asis('<?xml version="1.0" ?>\n')
doc.asis('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')

with tag('html', ('xml:lang', 'fr'), lang = 'fr', xmlns = 'http://www.w3.org/1999/xhtml'):
    with tag('head'):
        with tag('title'):
            text("Mercredi Fiction")
        with tag('link', rel = "stylesheet", type="text/css", href="mercredifiction.css"):
            pass
        with tag('meta', ('http-equiv', "Content-Type"), content = "text/html; charset=UTF-8"):
            pass
    text('\n')
    epubs = {}
    htmls = {}
    with tag('body'):
        for file in os.listdir('.'):
               result = re.search("-([0-9-]+)\.epub", file)
               if result:                
                  epubs[result.group(1)] = file
        sortedepubdates = sorted(epubs, reverse=True)
        for file in os.listdir('.'):
               result = re.search("-([0-9-]+)\.html", file)
               if result:                
                  htmls[result.group(1)] = file
        sortedhtmldates = sorted(htmls, reverse=True)
        with tag('h1'):
            text("Mercredi Fiction")    
        text('\n')
        with tag('p'):
            with tag('a', href = "#HTML"):
                text("Versions HTML")
        with tag('hr'):
            pass
        with tag('h2'):
            text("Versions EPUB")
        if os.path.exists(LASTEPUB):
            os.remove(LASTEPUB)
        os.symlink(epubs[sortedepubdates[0]], LASTEPUB)
        with tag('p'):
            with tag('a', href = LASTEPUB):
                text("Dernière version")
            text(" (le %s)" % formatdate(sortedepubdates[0]))
        text('\n')
        with tag('p'):
            text("Versions précédentes")
        with tag('ul'):
            text('\n')
            for date in sortedepubdates[1:]:
                with tag('li'):
                    with tag('a', href = epubs[date]):
                        text("Pouètes du %s" % formatdate(date))
                text('\n')
            text('\n')
        with tag('p'):
            with tag('a', name="HTML"):
                pass
        with tag('h2'):
            text("Versions HTML")
        if os.path.exists(LASTHTML):
            os.remove(LASTHTML)
        os.symlink(htmls[sortedhtmldates[0]], LASTHTML)
        with tag('p'):
            with tag('a', href = LASTHTML):
                text("Dernière version")
            text(" (le %s)" % formatdate(sortedhtmldates[0]))
        text('\n')
        with tag('p'):
            text("Versions précédentes")
        with tag('ul'):
            text('\n')
            for date in sortedhtmldates[1:]:
                with tag('li'):
                    with tag('a', href = htmls[date]):
                        text("Pouètes du %s" % formatdate(date))
                text('\n')
            text('\n')
        with tag('hr'):
            pass
        with tag('p'):
            text("Code disponible ")
            with tag('a', href = "https://github.com/bortzmeyer/MercrediFiction"):
                text("sur Github")
            text(", avec ")
            with tag('a', href="http://www.bortzmeyer.org/mastodon-mercredifiction.html"):
                text("explications")
            text(".")    
        with tag('hr'):
            pass
        with tag('p'):
            text("Autres distributions de pouètes #MercrediFiction :")
        with tag('ul'):
            with tag('li'):
                with tag('a', href = "https://mercredifiction.io/"):
                    text("mercredifiction.io (en cours de développement)")
        with tag('hr'):
            pass
        with tag('p'):
            text("Service maintenu par Stéphane Bortzmeyer, courrier à <stephane+mercredifiction@bortzmeyer.org>, Mastodon à ")
            with tag('code'):
                 with tag('a', href="https://mastodon.gougere.fr/@bortzmeyer"):
                     text("bortzmeyer@mastodon.gougere.fr")
            text(". Les pouètes sont écrits par divers auteurs, pas par moi. Chacun a donc sa propre licence.")

text('\n')
outfile = open(INDEX, 'w')
outfile.write(doc.getvalue())
outfile.close()

