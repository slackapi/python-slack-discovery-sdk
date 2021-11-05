# Copyright 2021, Slack Technologies, LLC. All rights reserved.

#!/bin/bash

script_dir=`dirname $0`
cd ${script_dir}/..
rm -rf ./slack_discovery_sdk.egg-info

pip install -U pip && \
  pip install twine wheel && \
  rm -rf dist/ build/ slack_discovery_sdk.egg-info/ && \
  python setup.py sdist bdist_wheel && \
  twine check dist/* && \
  twine upload dist/*