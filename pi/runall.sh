#!/bin/env sh

if [[ $# == 0 ]]; then
    trials=1000000;
    (>&2 echo -e "WARNING: no argument provided; using $trials trials\n");
else
    trials=$1;
fi

pushd C >/dev/null
    echo "Computing π in C:"
    time sh pi.sh $trials
popd >/dev/null

pushd "C++" >/dev/null
    echo -e "\nComputing π in C++:"
    time sh pi.sh $trials
popd >/dev/null

pushd Python >/dev/null
    echo -e "\nComputing π (for-loop) in Python 2.7:"
    time python36 pi.py $trials

    echo -e "\nComputing π (for-loop) in Python 3.6:"
    time python36 pi.py $trials

    echo -e "\nComputing π (vectorized) in Python 2.7:"
    time python36 pi-numpy.py $trials

    echo -e "\nComputing π (vectorized) in Python 3.6:"
    time python36 pi-numpy.py $trials
popd >/dev/null

pushd Julia >/dev/null
    echo -e "\nComputing π (for-loop) in Julia 0.6.2:"
    time julia pi.jl $trials

    echo -e "\nComputing π (vectorized) in Julia 0.6.2:"
    time julia pi-vec.jl $trials
popd >/dev/null

pushd R >/dev/null
    echo -e "\nComputing π (for-loop) in R:"
    time Rscript pi.r $trials

    echo -e "\nComputing π (vectorized) in R:"
    time Rscript pi-vec.r $trials
popd >/dev/null
