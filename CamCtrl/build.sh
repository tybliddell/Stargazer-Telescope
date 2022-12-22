#! /usr/bin/env bash
mkdir -p bin
go mod tidy
go build -o bin/camctrl main.go