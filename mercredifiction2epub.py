#!/usr/bin/python3
# -*- coding: utf-8 -*-

# [Used for a french-specific purpose, so all comments are in french.]

# Transformer les hstoires étiquetées #MercrediFiction de Mastodon en
# un livre EPUB. Stéphane Bortzmeyer <stephane@bortzmeyer.org>.

# TODO ajouter un mot sur le fait qu'on n'a que son instance

# Le fichier "log" est récolté par des appels périodiques à :
#    madonctl --output json timeline :mercredifiction

# Documents utiles à lire sur la génération d'EPUB :
# http://www.hxa.name/articles/content/epub-guide_hxa7241_2007.html
# https://gist.github.com/anqxyr/6c70a2e4e8209cd43fc1

# Pour valider : en ligne avec http://validator.idpf.org/application/validate
# ou localement avec einfo (paquetage Debian epub-utils) mais il n'attrappe pas autant de problèmes.

# Standard library
import json
import zipfile
import time
from io import StringIO

# Other libraries
from lxml.html.clean import Cleaner
from lxml import etree, html
# http://www.yattag.org/
# But Jinja2 seems far more popular
from yattag import Doc

LOG = "mercredifiction.log"
JSON = "mercredifiction.json"
HTML = "mercredifiction.html"
EPUB = "mercredifiction.epub"
CSS = "mercredifiction.css"
OPF = "content.opf"
TOC = "toc.ncx"

infile = open(LOG, 'r')
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

infile = open(JSON, 'r')
uris = {}
doc, tag, text = Doc().tagtext()
data = json.load(infile)
doc.asis('<?xml version="1.0" ?>\n')
doc.asis('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n')
with tag('html', ('xml:lang', 'fr'), xmlns = 'http://www.w3.org/1999/xhtml'):
    with tag('head'):
        with tag('title'):
            text("Mercredi Fiction")
    text('\n')
    with tag('body'):
        with tag('h1'):
            text("Mercredi Fiction")
        text('\n')
        for toots in data:
            for toot in toots:
                uri = toot["uri"]
                if uri not in uris: # TODO supprimer des pouètes comme le TrendingTopic
                    with tag('h2'):
                        text("Par %s <%s> le %s" % (toot["account"]["display_name"], toot["account"]["acct"],
                                                    toot["created_at"])) # TODO: format the date
                    text('\n')
                    # Les pouètes contiennent de l'HTML, ce qui est vraiment une mauvaise idée (même pas du XHTML)
                    cleaner = Cleaner(scripts=True, javascript=True, embedded=True, meta=True, page_structure=True,
                                      links=False, remove_unknown_tags=True,
                                      style=False)
                    content = cleaner.clean_html(toot["content"])
                    with tag('div', klass = 'content'):
                        # Convert to XHTML
                        tree = html.fromstring(content)
                        result = etree.tostring(tree, pretty_print=False, method="xml")
                        doc.asis(result.decode('UTF-8'))
                    text('\n')
                    with tag('p', klass = 'url'):
                        with tag('a', href = toot["url"]):
                            text("Lien original")
                    text('\n')
                    uris[uri] = True
outfile = open(HTML, 'w')
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
                 text("Mercredi Fiction") # TODO ajouter la date
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
          text(time.strftime('%Y-%m-%d', time.gmtime(time.time())))
      with tag('dc:rights'):
        text("Chaque pouète reste avec sa propre licence")
    with tag('manifest'):
        with tag('item', ('media-type', "text/css"), id = 'css', href = CSS):
                 pass
        with tag('item', ('media-type', "application/xhtml+xml"), id = 'contents', href = HTML):
                 pass
        with tag('item', ('media-type', "application/x-dtbncx+xml"), id = 'ncx',  href = "toc.ncx"):
                 pass
    with tag('spine', toc = 'ncx'):
        with tag('itemref', idref = 'contents'):
            pass
    with tag('guide'):
        with tag('reference', type = "text", title = "Text", href = HTML):
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
            text("Mercredi Fiction") # TODO date
    with tag('navMap'):
        with tag('navPoint', id = "navPoint-1", playOrder = "1"):
            with tag('navLabel'):
                with tag('text'):
                    text("Mercredi Fiction")
            with tag('content', src = HTML):
                pass
outfile = open(TOC, 'w')
outfile.write(doc.getvalue())
outfile.close()  

with zipfile.ZipFile(EPUB, 'w') as myzip:
    myzip.write('mimetype', compress_type=None)
    for file in ['META-INF/container.xml', OPF, HTML, CSS, TOC]:
        myzip.write(file)
    myzip.close()
    
