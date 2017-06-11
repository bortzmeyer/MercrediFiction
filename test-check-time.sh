#!/bin/sh

. ./check-time.sh

if [ -z "$1" ]; then
    echo "Usage: $0 expectedtime" >&2
    exit 1
fi

if check_time $1; then
    echo "To do"
else
    echo "Not yet or too late"
fi

