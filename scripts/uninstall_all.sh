#!/bin/bash

pip uninstall -y slack-discovery-sdk

PACKAGES=$(pip freeze | grep -v "^-e" | sed 's/@.*//' | sed 's/\=\=.*//')

for package in $PACKAGES; do
  pip uninstall -y $package
done
