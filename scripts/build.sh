#!/bin/bash

script_dir=`dirname $0`
cd ${script_dir}/..
version=`grep __version__ ./slack_discovery_sdk/version.py | awk -F'"' '{print $2}'`
while true; do
    read -p "Do you wish to build a package for version ${version}? (y/N)" yn
    case $yn in
        [Yy]* ) make install; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

pip install twine wheel && \
  rm -rf ./dist/ ./build/ *.egg-info/ && \
  python setup.py sdist bdist_wheel && \
  twine check dist/*
