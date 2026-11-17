#!/bin/bash
script_dir=$(dirname $0)
cd ${script_dir}/..

# Clean previous builds
rm -rf dist/ build/ slack_discovery_sdk.egg-info/

# Install build dependencies unless --no-install is specified
if [[ "$1" != "--no-install" ]]; then
    pip install -r requirements/build.txt
fi

# Build package
python -m build && twine check dist/*
