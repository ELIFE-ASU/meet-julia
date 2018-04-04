#!/bin/env sh

if [[ $# == 0 ]]; then
    trials=10000000;
    (>&2 echo -e "WARNING: no argument provided; using $trials trials\n");
else
    trials=$1;
fi

echo "Computing π in C:"
time sh pi-c.sh $trials
