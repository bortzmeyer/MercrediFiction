#!/usr/bin/python3
# -*- coding: utf-8 -*-

# [Used for a french-specific purpose, so all comments are in french.]

# Transformer les hstoires étiquetées #MercrediFiction de Mastodon en
# un livre EPUB ou en pages HTML. Stéphane Bortzmeyer
# <stephane@bortzmeyer.org>.

# Le fichier "log" est récolté par des appels périodiques à :
#    madonctl --output json timeline :mercredifiction
# Attention: cela ne donne que les pouètes qui sont sur l'instance
# qu'interroge madonctl.  Il vaut donc mieux choisir une instance
# « importante ».

# Documents utiles à lire sur la génération d'EPUB :
# http://www.hxa.name/articles/content/epub-guide_hxa7241_2007.html
# https://gist.github.com/anqxyr/6c70a2e4e8209cd43fc1

# Pour valider : en ligne avec
# http://validator.idpf.org/application/validate ou localement avec
# einfo (paquetage Debian epub-utils) mais il n'attrape pas autant de
# problèmes ou encore epubcheck (paquetage Debian du même nom).

# Standard library
import json
import zipfile
import time
import sys
import re
import locale
from io import StringIO

# Other libraries
from lxml.html.clean import Cleaner
from lxml import etree, html
# http://www.yattag.org/
# But Jinja2 seems far more popular
from yattag import Doc

LOG = "mercredifiction-%s.log"
JSON = "mercredifiction.json"
HTML = "mercredifiction-%s.html"
EPUB = "mercredifiction-%s.epub"
CSS = "mercredifiction.css"
OPF = "content.opf"
TOC = "toc.ncx"
RFC3339DATE = "%Y-%m-%d"
RFC3339DATETIME = "%Y-%m-%dT%H:%M:%SZ"
BLOCKLIST = ["TrendingBot@mastodon.social",]

def samedate(left, right):
    return (left.tm_year == right.tm_year and left.tm_mon==right.tm_mon and left.tm_mday == right.tm_mday)

def cleandate(str):
    # En dépit de ce que dit la documentation, les secondes
    # fractionnaires ne sont pas acceptées, il faut donc les retirer
    return(re.sub('\.[0-9]+Z$', 'Z', str))

def formatdate(str, short=False):
    try:
        bdate = time.strptime(cleandate(str), RFC3339DATETIME)
    except ValueError:
        bdate = time.strptime(cleandate(str), RFC3339DATE)
    if short:
        return time.strftime("%d %B %Y", bdate)
    else:
        return time.strftime("%d %B %Y à %H h %M UTC", bdate)

locale.setlocale(locale.LC_TIME, 'fr_FR')
  
if len(sys.argv) != 2:
    sys.stderr.write("Usage: %s date-in-rfc-3339-format\n" % sys.argv[0])
    sys.exit(1)
date = time.strptime(sys.argv[1], RFC3339DATE)
datestr = time.strftime(RFC3339DATE, date)

# On ramasse les pouètes par des appels à madonctl qu'on concatène. Le
# résultat (LOG) n'est donc pas du JSON, on le transforme donc en
# tableau JSON.
infile = open(LOG % datestr, 'r')
outfile = open(JSON, 'w')
outfile.write('[')
first = True
for line in infile.readlines():
    if not first:
        outfile.write(",\n")
    else:
        first = False
    outfile.write(line)
infile.close()
outfile.write(']')
outfile.close()

# Transformer le JSON en HTML
infile = open(JSON, 'r')
uris = {}
doc, tag, text = Doc().tagtext()
data = json.load(infile)
doc.asis('<?xml version="1.0" ?>\n')
doc.asis('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n')
with tag('html', ('xml:lang', 'fr'), xmlns = 'http://www.w3.org/1999/xhtml'):
    with tag('head'):
        with tag('link', rel = "stylesheet", type = "text/css", href = "mercredifiction.css"):
            pass
        with tag('title'):
            text("Mercredi Fiction %s" % datestr)
    text('\n')
    with tag('body'):
        with tag('h1'):
            text("Mercredi Fiction du %s" % formatdate(datestr, short=True))
        text('\n')
        numtoots = 0
        for toots in data:
            for toot in toots:
                uri = toot["uri"]
                if uri not in uris and \
                   samedate(date, time.strptime(cleandate(toot["created_at"]), RFC3339DATETIME)) and \
                   toot["account"]["acct"] not in BLOCKLIST:
                    with tag('h2'):
                        text("Par %s <%s> le %s" % (toot["account"]["display_name"], toot["account"]["acct"],
                                                    formatdate(toot["created_at"]))) 
                    text('\n')
                    # Les pouètes contiennent de l'HTML, ce qui est vraiment une mauvaise idée (même pas du XHTML).
                    # TODO : il faudrait aussi supprimer les attributs target des <a>, qui n'existent pas en XHTML strict, et empêchent une validation parfaite
                    cleaner = Cleaner(scripts=True, javascript=True, embedded=True, meta=True, page_structure=True,
                                      links=False, remove_unknown_tags=True,
                                      style=False)
                    content = cleaner.clean_html(toot["content"])
                    with tag('div', klass = 'content'):
                        # Conversion en XHTML
                        tree = html.fromstring(content)
                        result = etree.tostring(tree, pretty_print=False, method="xml")
                        doc.asis(result.decode('UTF-8'))
                    text('\n')
                    with tag('p', klass = 'url'):
                        with tag('a', href = toot["url"]):
                            text("Lien original")
                    text('\n')
                    uris[uri] = True
                    numtoots += 1
        with tag('hr'):
            pass
        with tag('p', klass = "summary"):
            text("(%d pouètes en tout)" % numtoots)
outfile = open(HTML % datestr, 'w')
infile.close()
outfile.write(doc.getvalue())
outfile.close()

doc, tag, text = Doc().tagtext()
doc.asis('<?xml version="1.0" ?>\n')
with tag('package', ('unique-identifier', 'dcidid'), xmlns = 'http://www.idpf.org/2007/opf', version = "2.0"):
    with tag('metadata', ('xmlns:dc', "http://purl.org/dc/elements/1.1/"),
             ('xmlns:dcterms', "http://purl.org/dc/terms/"),
             ('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance"),
             ('xmlns:opf', "http://www.idpf.org/2007/opf")):
      with tag('dc:title'):
                 text("Mercredi Fiction %s" % datestr) 
      with tag('dc:language', ('xsi:type', "dcterms:RFC3066")):
                 text("fr")
      with tag('dc:identifier', ('opf:scheme', "URI"), id = "dcidid"):
          text("tag:mercredifiction.bortzmeyer.org,2017-05:/")
      with tag('dc:subject'):
          text("Fiction")
      with tag('dc:description'):
          text("Collection des pouètes envoyés sur Mastodon avec le mot-croisillon #MercrediFiction")
      with tag('dc:creator'):
          text("Stéphane Bortzmeyer")
      with tag('dc:publisher'):
          text("Stéphane Bortzmeyer")
      with tag('dc:date', ('xsi:type', "dcterms:W3CDTF")):
          text(time.strftime(RFC3339DATE, time.gmtime(time.time())))
      with tag('dc:rights'):
        text("Chaque pouète reste avec sa propre licence")
    with tag('manifest'):
        with tag('item', ('media-type', "text/css"), id = 'css', href = CSS):
                 pass
        with tag('item', ('media-type', "application/xhtml+xml"), id = 'contents', href = HTML % datestr):
                 pass
        with tag('item', ('media-type', "application/x-dtbncx+xml"), id = 'ncx',  href = "toc.ncx"):
                 pass
    with tag('spine', toc = 'ncx'):
        with tag('itemref', idref = 'contents'):
            pass
    with tag('guide'):
        with tag('reference', type = "text", title = "Text", href = HTML % datestr):
            pass
outfile = open(OPF, 'w')
outfile.write(doc.getvalue())
outfile.close()  

doc, tag, text = Doc().tagtext()
doc.asis('<?xml version="1.0" ?>\n')
doc.asis('<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"  "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">\n')
with tag('ncx', xmlns = "http://www.daisy.org/z3986/2005/ncx/", version = "2005-1"):
    with tag('head'):
        with tag('meta', name = "dtb:uid", content="tag:mercredifiction.bortzmeyer.org,2017-05:"):
            pass
        with tag('meta', name = "dtb:depth", content="1"):
            pass
        with tag('meta', name = "dtb:totalPageCount", content="0"):
            pass
        with tag('meta', name = "dtb:maxPageNumber", content="0"):
            pass
    with tag('docTitle'):
        with tag('text'):
            text("Mercredi Fiction %s" % datestr) 
    with tag('navMap'):
        with tag('navPoint', id = "navPoint-1", playOrder = "1"):
            with tag('navLabel'):
                with tag('text'):
                    text("Mercredi Fiction %s" % datestr)
            with tag('content', src = HTML % datestr):
                pass
outfile = open(TOC, 'w')
outfile.write(doc.getvalue())
outfile.close()  

with zipfile.ZipFile(EPUB % datestr, 'w') as myzip:
    myzip.write('mimetype', compress_type=None)
    for file in ['META-INF/container.xml', OPF, HTML % datestr, CSS, TOC]:
        myzip.write(file)
    myzip.close()
    
