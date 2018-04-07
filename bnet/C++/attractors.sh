#!/bin/env sh

g++ -std=c++17 -Wall -O3 -o attractors attractors.cpp -lm
./attractors $1 $2
rm attractors
