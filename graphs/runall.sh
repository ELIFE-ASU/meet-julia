#!/bin/env sh

if [[ $# -lt 3 ]]; then
    (>&2 echo -e "usage: runall.sh <n> <k> <seed>");
    exit 1
else
    n=$1
    k=$2
    seed=$3
fi

echo -e "\nEvaluating NetworkX in Python 2.7:"
time python27 netx.py $n $k $seed

echo -e "\nEvaluating NetworkX in Python 3.6:"
time python36 netx.py $n $k $seed

echo -e "\nEvaluting LightGraphs.jl in Julia 0.6.2:"
time julia lightgraphs.jl $n $k $seed
