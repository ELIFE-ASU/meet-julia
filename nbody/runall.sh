#!/bin/env sh

if [[ $# -lt 1 ]]; then
    (>&2 echo -e "ERROR: must provide a data file\n");
    exit 1;
elif [[ $# -eq 1 ]]; then
    filename=$1;
    timesteps=1000000;
    (>&2 echo -e "WARNING: no argument provided; using $timesteps timesteps\n");
else
    filename=$1;
    timesteps=$2;
fi

pushd C >/dev/null
    echo "Running n-body simulation in C:"
    time sh nbody.sh ../$filename $timesteps
popd >/dev/null

echo -e "\nRunning n-body simulation in Python 2.7:"
time python27 nbody.py $filename $timesteps

echo -e "\nRunning n-body simulation in Python 3.6:"
time python36 nbody.py $filename $timesteps

echo -e "\nRunning n-body simulation in Julia 0.6.2:"
time julia nbody.jl $filename $timesteps
