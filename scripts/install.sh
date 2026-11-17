#!/bin/bash
script_dir=$(dirname $0)
cd ${script_dir}/..

pip install -U pip
pip install -e .
pip install -r requirements/testing.txt
pip install -r requirements/dev-tools.txt
