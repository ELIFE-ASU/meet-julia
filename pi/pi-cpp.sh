#!/bin/env sh

g++ -std=c++11 -O3 -o pi pi.cpp
./pi $1
rm pi
