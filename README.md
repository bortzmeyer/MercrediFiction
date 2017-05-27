# MercrediFiction

(The Mercredi Fiction toots are in french so all the documentation here is in french.)

Outils pour transformer les #MercrediFiction de Mastodon en autres formats

Voir les commentaires dans les programmes.

## Installation locale

Il faut Python 3, [madonctl](https://github.com/McKael/madonctl), et les modules Python lxml et yattag.

TODO documenter la config crontab
 maybe with something like
* * * * * user [ $(($(date +\%H)+offset))  == 1400 ] && command
 et faire un exit 0 dans le script si ce n'est pas proche de la bonne heure en France (oui, c'est moche mais ça fonctionnera)

## Autres outils

Un autre outil (apparemment bien plus riche/complexe) est https://github.com/Meewan/MercrediFiction
