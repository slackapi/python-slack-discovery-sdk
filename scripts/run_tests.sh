#!/bin/bash
# all: ./scripts/run_tests.sh
# single: ./scripts/run_tests.sh tests/test_rate_limit_support.py

script_dir=$(dirname $0)
cd ${script_dir}/..

test_target="$1"

./scripts/format.sh --no-install

# Run tests
if [[ $test_target != "" ]]; then
  pytest -vv $test_target
else
  pytest
fi
