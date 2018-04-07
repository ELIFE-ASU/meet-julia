#!/bin/env sh

if [[ $# -lt 2 ]]; then
    (>&2 echo -e "ERROR: must provide a data file\n");
    exit 1;
else
    weights=$1;
    thresholds=$2;
fi

pushd "C++" >/dev/null
    echo "Running n-body simulation in C++:"
    time sh attractors.sh ../$weights ../$thresholds
popd >/dev/null

echo -e "\nRunning n-body simulation in Python 2.7:"
time python27 attractors.py $weights $thresholds

echo -e "\nRunning n-body simulation in Python 3.6:"
time python36 attractors.py $weights $thresholds

echo -e "\nRunning n-body simulation in Julia 0.6.2:"
time julia attractors.jl $weights $thresholds
