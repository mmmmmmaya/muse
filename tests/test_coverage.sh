#!/bin/bash

for filename in ./tests/*.py; do
    coverage run -p --source=. --omit=./env/* $filename
done

coverage combine
coverage report -m
coverage html
