#!/bin/bash
script_dir=$(dirname $0)
cd ${script_dir}/..

# Install dependencies unless --no-install is specified
if [[ "$1" != "--no-install" ]]; then
    ./scripts/install.sh
fi

mypy --config-file pyproject.toml
