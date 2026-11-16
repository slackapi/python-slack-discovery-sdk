#!/bin/bash
script_dir=$(dirname $0)
cd ${script_dir}/..

./scripts/build_pypi_package.sh

# Upload to test PyPI
twine upload --repository testpypi dist/*
