#! /usr/bin/env bash
mkdir -p bin
go mod tidy
go build -o bin/image_processor main.go