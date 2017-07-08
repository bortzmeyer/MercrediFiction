# MercrediFiction

(The Mercredi Fiction toots are in french so all the documentation here is in french.)

Outils pour transformer les #MercrediFiction de Mastodon en autres
formats (actuellement EPUB et HTML). Le résultat est [visible ici](http://mercredifiction.bortzmeyer.org/).

Voir les commentaires dans les programmes.

## Installation locale

Il faut Python 3, [madonctl](https://github.com/McKael/madonctl), et les modules Python lxml et yattag.

Il faut d'abord configurer madonctl avec votre instance (regardez la
documentation de ce programme mais, en gros, en supposant que votre
compte ait été créé avec l'adresse `mercredifiction@example.com` et
qu'il soit chez [Framapiaf](https://framapiaf.org/about), c'est du genre `madonctl config dump -i framapiaf.org -L mercredifiction@example.com -P SECRET > $HOME/.config/madonctl/madonctl.yaml`.

Ensuite, on exécute en général les scripts depuis cron, par exemple, sur une machine qui
est à l'heure légale française :

```
0 0 * * Wed (cd ./MercrediFiction; date '+%Y-%m-%d' > LAST)
29,59 0-23 * * Wed (cd ./MercrediFiction; ./ramassemercredifiction.sh $(cat ./LAST))
0 0 * * Thu (cd ./MercrediFiction; ./mercredifiction2others.py $(cat ./LAST) ; ./faireindex.py)
```

Si la machine est en UTC et qu'on veut quand même ramasser uniquement
le mercredi, on peut par exemple utiliser le script `check-time.sh` et
avoir une crontab comme :

```
1 23 * * Tue (cd ./MercrediFiction; ./create-last.sh 0000)
1 22 * * Tue (cd ./MercrediFiction; ./create-last.sh 0000)
2,32 22-23 * * Tue (cd ./MercrediFiction; if [ -e LAST ]; then ./ramassemercredifiction.sh $(cat ./LAST); fi)
2,32 0-23 * * Wed (cd ./MercrediFiction; if [ -e LAST ]; then ./ramassemercredifiction.sh $(cat ./LAST); fi)
0 22 0 * * Wed (cd ./MercrediFiction; ./create-epub.sh 0000)
0 23 0 * * Wed (cd ./MercrediFiction; ./create-epub.sh 0000)
```

(Avec `create-epub.sh un script qui utilise `check-time.sh`, puis appelle ̀mercredifiction2others.py` et `faireindex.py` regardez `create-last.sh` pour voir comment faire.)


## Autres outils

Un autre outil (apparemment bien plus riche/complexe) est https://github.com/Meewan/MercrediFiction
