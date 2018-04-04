#!/bin/env sh

gcc -std=c11 -O3 -o pi pi.c
./pi $1
rm pi
