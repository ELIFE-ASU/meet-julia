#!/bin/env sh

gcc -std=c11 -Wall -O3 -o nbody nbody.c -lm -ljson-c
./nbody $1 $2
rm nbody
