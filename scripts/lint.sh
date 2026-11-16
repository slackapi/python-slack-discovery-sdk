#!/bin/bash
script_dir=$(dirname $0)
cd ${script_dir}/..

# Install dependencies unless --no-install is specified
if [[ "$1" != "--no-install" ]]; then
    pip install -U pip
    pip install -r requirements/dev-tools.txt
fi

ruff check slack_discovery_sdk/ tests/ && ruff format --check slack_discovery_sdk/ tests/
