#! /usr/bin/env bash

base=${1%.*}
ext=${1#$base.}

if [[ "$ext" == "go" ]]
then
go build -gcflags=all="-N -l -r" -o "${base}.dbg"
else
gcc -lraw -g -O0 "${base}.${ext}" -o "${base}.dbg"
fi
