#!/bin/sh

BASEDIR=$HOME/Programmation/MercrediFiction
if [ -z "$1" ]; then
    echo "Usage: $0 date"
    exit 1
fi
LOG=mercredifiction-${1}.log

cd ${BASEDIR}

madonctl --output json timeline :MercrediFiction >> ${LOG}
