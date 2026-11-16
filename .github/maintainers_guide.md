# Maintainers Guide

This document describes tools, tasks and workflow that one needs to be familiar with in order to effectively maintain
this project. If you use this package within your own software as is but don't plan on modifying it, this guide is
**not** for you.

## Tools

### Python (and friends)

We recommend using [pyenv](https://github.com/pyenv/pyenv) for Python runtime management. If you use macOS, follow the following steps:

```sh
brew update
brew install pyenv
```

Install necessary Python runtimes for development/testing. You can rely on GitHub Actions for testing with various major versions.

```sh
pyenv install -l | grep -v "-e[conda|stackless|pypy]"

pyenv install 3.9.18 # select the latest patch version
pyenv local 3.9.18

pyenv versions
  system
  3.6.10
  3.7.7
* 3.9.18 (set by /path-to-python-slack-discovery-sdk/.python-version)

pyenv rehash
```

Then, you can create a new Virtual Environment this way:

```sh
python -m venv env_3.9.18
source env_3.9.18/bin/activate
```

## Tasks

### Testing

#### Run All the Unit Tests

If you make some changes to this project, please write corresponding unit tests as much as possible. You can easily run all the tests by running the following scripts.

If this is your first time to run tests, although it may take a bit longer, running the following script is the easiest.

```sh
./scripts/install_and_run_tests.sh
```

To simply install all the development dependencies for this project.

```sh
./scripts/install.sh
```

Once you installed all the required dependencies, you can use the following.

```sh
./scripts/run_tests.sh
./scripts/run_tests.sh tests/test_rate_limit_support.py
```

Tests marked `live` call the real Discovery API and are skipped unless `SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN` is set. See [Running tests](../README.md#running-tests) for the app and tokens they need.

To format this project

```sh
./scripts/format.sh
```

To lint this project

```sh
./scripts/lint.sh
```

This project uses [mypy](https://mypy.readthedocs.io/en/stable/index.html) to check and infers types for your Python code.

```sh
./scripts/run_mypy.sh
```

To clean your virtual environment (useful when testing scripts in isolation):

```sh
./scripts/uninstall_all.sh
```

> **Note**: Several scripts support a `--no-install` flag to prevent redundant dependency installation when scripts call other scripts internally.

#### Develop Locally

If you want to test the package locally you can.

1. Build the package locally

   - Run

     ```sh
     scripts/build_pypi_package.sh
     ```

   - This will create a `.whl` file in the `./dist` folder

2. Use the built package

   - Example `/dist/slack_discovery_sdk-1.2.3-py3-none-any.whl` was created
   - From anywhere on your machine you can install this package to a project with

     ```sh
     pip install <project path>/dist/slack_discovery_sdk-1.2.3-py3-none-any.whl
     ```

### Releasing

#### test.pypi.org deployment

[TestPyPI](https://test.pypi.org/) is a separate instance of the Python Package
Index that allows you to try distribution tools and processes without affecting
the real index. This is particularly useful when making changes related to the
package configuration itself, for example, modifications to the `pyproject.toml` file.

You can deploy this project to TestPyPI using GitHub Actions.

To deploy using GitHub Actions:

1. Push your changes to a branch or tag
2. Navigate to <https://github.com/slackapi/python-slack-discovery-sdk/actions/workflows/pypi-release.yml>
3. Click on "Run workflow"
4. Select your branch or tag from the dropdown
5. Click "Run workflow" to build and deploy your branch to TestPyPI

Alternatively, you can deploy from your local machine with:

```sh
./scripts/deploy_to_test_pypi.sh
```

#### Development Deployment

Deploying a new version of this library to PyPI is triggered by publishing a GitHub Release.
Before creating a new release, ensure that everything on a stable branch has
landed, then [run the tests](#run-all-the-unit-tests).

1. Create the commit for the release
   1. Use the latest supported Python version. Using a [virtual environment](#python-and-friends) is recommended.
   2. In `slack_discovery_sdk/version.py` bump the version number in adherence to [Semantic Versioning](http://semver.org/) and [Developmental Release](https://peps.python.org/pep-0440/#developmental-releases).
      - Example: if the current version is `1.2.3`, a proper development bump would be `1.2.4.dev0`
      - `.dev` will indicate to pip that this is a [Development Release](https://peps.python.org/pep-0440/#developmental-releases)
      - Note that the `dev` version can be bumped in development releases: `1.2.4.dev0` -> `1.2.4.dev1`
   3. Commit with a message including the new version number. For example `1.2.4.dev0` & push the commit to a branch where the development release will live (create it if it does not exist)
      1. `git checkout -b future-release`
      2. `git add --all` (review files with `git status` before committing)
      3. `git commit -m 'chore(release): version 1.2.4.dev0'`
      4. `git push -u origin future-release`
2. Create a new GitHub Release
   1. Navigate to the [Releases page](https://github.com/slackapi/python-slack-discovery-sdk/releases).
   2. Click the "Draft a new release" button.
   3. Set the "Target" to the feature branch with the development changes.
   4. Click "Tag: Select tag"
   5. Input a new tag name manually. The tag name must match the version in `slack_discovery_sdk/version.py` prefixed with "v" (e.g., if version is `1.2.4.dev0`, enter `v1.2.4.dev0`)
   6. Click the "Create a new tag" button. This won't create your tag immediately.
   7. Click the "Generate release notes" button.
   8. The release name should match the tag name!
   9. Edit the resulting notes to ensure they have decent messaging that is understandable by non-contributors, but each commit should still have its own line.
   10. Set this release as a pre-release.
   11. Publish the release by clicking the "Publish release" button!
3. Navigate to the [release workflow run](https://github.com/slackapi/python-slack-discovery-sdk/actions/workflows/pypi-release.yml). You will need to approve the deployment!
4. After a few minutes, the corresponding version will be available on <https://pypi.org/project/slack-discovery-sdk>.
5. (Slack Internal) Communicate the release internally

#### Production Deployment

Deploying a new version of this library to PyPI is triggered by publishing a GitHub Release.
Before creating a new release, ensure that everything on the `main` branch since
the last tag is in a releasable state! At a minimum, [run the tests](#run-all-the-unit-tests).

1. Create the commit for the release
   1. Use the latest supported Python version. Using a [virtual environment](#python-and-friends) is recommended.
   2. In `slack_discovery_sdk/version.py` bump the version number in adherence to [Semantic Versioning](http://semver.org/) and the [Versioning](#versioning-and-tags) section.
   3. Commit with a message including the new version number. For example `1.2.3` & push the commit to a branch and create a PR to sanity check.
      1. `git checkout -b 1.2.3-release`
      2. `git add --all` (review files with `git status` before committing)
      3. `git commit -m 'chore(release): version 1.2.3'`
      4. `git push -u origin 1.2.3-release`
   4. Add relevant labels to the PR and add the PR to a GitHub Milestone.
   5. Merge in release PR after getting an approval from at least one maintainer.
2. Create a new GitHub Release
   1. Navigate to the [Releases page](https://github.com/slackapi/python-slack-discovery-sdk/releases).
   2. Click the "Draft a new release" button.
   3. Set the "Target" to the `main` branch.
   4. Click "Tag: Select tag"
   5. Input a new tag name manually. The tag name must match the version in `slack_discovery_sdk/version.py` prefixed with "v" (e.g., if version is `1.2.3`, enter `v1.2.3`)
   6. Click the "Create a new tag" button. This won't create your tag immediately.
   7. Click the "Generate release notes" button.
   8. The release name should match the tag name!
   9. Edit the resulting notes to ensure they have decent messaging that is understandable by non-contributors, but each commit should still have its own line.
   10. Include a link to the current GitHub Milestone.
   11. Ensure the "latest release" checkbox is checked to mark this as the latest stable release.
   12. Publish the release by clicking the "Publish release" button!
3. Navigate to the [release workflow run](https://github.com/slackapi/python-slack-discovery-sdk/actions/workflows/pypi-release.yml). You will need to approve the deployment!
4. After a few minutes, the corresponding version will be available on <https://pypi.org/project/slack-discovery-sdk>.
5. Close the current GitHub Milestone and create one for the next patch version.
6. (Slack Internal) Communicate the release internally
    - Include a link to the GitHub release
7. (Slack Internal) Tweet by @SlackAPI
    - Not necessary for patch updates, might be needed for minor updates,
      definitely needed for major updates. Include a link to the GitHub release

## Workflow

### Versioning and Tags

This project uses [Semantic Versioning](http://semver.org/), expressed through the numbering scheme of
[PEP-0440](https://www.python.org/dev/peps/pep-0440/).

### Branches

`main` is where active development occurs. Long running named feature branches are occasionally created for
collaboration on a feature that has a large scope (because everyone cannot push commits to another person's open Pull
Request). At some point in the future after a major version increment, there may be maintenance branches for older major
versions.

## Everything else

When in doubt, find the other maintainers and ask.
