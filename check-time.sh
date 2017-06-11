#!/bin/sh

# Vérifie l'heure en heure légale (sur une machine UTC) et sort si ce
# n'est pas l'heure attendue. L'idée est d'être lancé par cron aux
# deux heures UTC possibles pour une heure légale française (cron ne
# traite pas la variable TZ ni CRON_TZ).

export TZ=Europe/Paris

check_time()
{
   if [ -z "$1" ]; then
       echo "Usage: $0 expectedtime" >&2
       exit 1
   fi
   exptime=$(date -d $1 +%s)
   if [ -z "$exptime" ]; then
       echo "Wrong time format $1" >&2
       exit 1
   fi
   lasttime=$(echo $exptime+300 | bc)

   curdatetime=$(date +%s)
   
   if [ $curdatetime -le $exptime ]; then
       return 1 # Not yet
   fi
   if [ $curdatetime -ge $lasttime ]; then
       return 2 # Too late
   else
       return 0 # Good
   fi
}
