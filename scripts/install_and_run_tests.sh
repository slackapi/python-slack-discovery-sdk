#!/bin/bash
# all: ./scripts/install_and_run_tests.sh
# single: ./scripts/install_and_run_tests.sh tests/test_rate_limit_support.py

script_dir=$(dirname $0)
cd ${script_dir}/..

test_target="$1"

./scripts/install.sh
./scripts/format.sh --no-install
./scripts/lint.sh --no-install

# Run tests
if [[ $test_target != "" ]]; then
  pytest -vv $test_target
else
  pytest
  ./scripts/run_mypy.sh --no-install
fi
