#!/bin/sh

. ./check-time.sh

if check_time $1; then
    date '+%Y-%m-%d' > LAST
fi

