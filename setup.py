#!/usr/bin/env python
import os

import setuptools

here = os.path.abspath(os.path.dirname(__file__))

__version__ = None
exec(open(f"{here}/slack_discovery_sdk/version.py").read())

with open(f"{here}/README.md", "r") as fh:
    long_description = fh.read()

test_dependencies = [
    "pytest>=5,<6",
    "pytest-cov>=2,<3",
    "black==21.5b1",
]

setuptools.setup(
    name="slack-discovery-sdk",
    version=__version__,
    author="Slack Technologies, Inc.",
    author_email="opensource@slack.com",
    description="The Slack Discovery API SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(
        exclude=[
            "tests",
            "tests.*",
        ]
    ),
    include_package_data=True,  # MANIFEST.in
    install_requires=[
        "slack_sdk>=3.8.0,<4",
    ],
    setup_requires=["pytest-runner==5.2"],
    tests_require=test_dependencies,
    test_suite="tests",
    extras_require={
        # pip install -e ".[testing]"
        "testing": test_dependencies,
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)