# Contributors Guide

Interested in contributing? Awesome! Before you do though, please read our [Code of Conduct](https://slackhq.github.io/code-of-conduct). We take it very seriously, and expect that you will as well.

> 🚨 Note: If you are not a project maintainer (i.e. you do not work at Slack), please use [this issue form](https://forms.gle/jHS17eYEYAtcXA96A), or for feedback, please use [this feedback form](https://forms.gle/B2PRF9HQheRgQdo7A). This SDK is only accessible to customer developers with access to the Discovery API (Enterprise accounts) or partners who have been onboarded to the Security and Compliance partner program. To learn more about the Discovery APIs, please [visit our help center](https://slack.com/help/articles/360002079527-A-guide-to-Slacks-Discovery-APIs). 🚨

There are many ways you can contribute! :heart:

### Bug Reports and Fixes :bug:

- If you find a bug, please report it using [this issue form](https://forms.gle/jHS17eYEYAtcXA96A).
- If you'd like to submit a fix for a bug, [send a Pull Request](#creating-a-pull-request).
- Include tests that isolate the bug and verifies that it was fixed.

### New Features :bulb:

- If you'd like to add new functionality to this project, describe the problem you want to solve using [this feedback form](https://forms.gle/B2PRF9HQheRgQdo7A).
- If you'd like to implement the new feature, please wait for feedback from the project maintainers before spending too much time writing the code. In some cases, enhancements may not align well with the project objectives at the time.

### Tests :mag:, Documentation :books:, Miscellaneous :sparkles:

- If you'd like to improve the tests, you want to make the documentation clearer, you have an alternative implementation of something that may have advantages over the way its currently done, or you have any other change, we would be happy to hear about it!
- If its a trivial change, go ahead and [send a Pull Request](#creating-a-pull-request) with the changes you have in mind.
- If not, share the idea using [this feedback form](https://forms.gle/B2PRF9HQheRgQdo7A) first.

## Requirements

For your contribution to be accepted:

- [x] You must have signed the [Contributor License Agreement (CLA)](https://cla.salesforce.com/sign-cla).
- [x] The test suite must be complete and pass (see [Running tests](https://github.com/slackapi/python-slack-discovery-sdk#running-tests) for details on how to run the tests).
- [x] The changes must be approved by code review.
- [x] Commits should be atomic and messages must be descriptive.

If the contribution doesn't meet the above criteria, you may fail our automated checks or a maintainer will discuss it with you. You can continue to improve a Pull Request by adding commits to the branch from which the PR was created.

[Interested in knowing more about about pull requests at Slack?](https://slack.engineering/on-empathy-pull-requests-979e4257d158#.awxtvmb2z)

## Creating a Pull Request

1. :fork_and_knife: Fork the repository on GitHub.
2. :runner: Clone/fetch your fork to your local development machine. It's a good idea to run the tests just to make sure everything is in order.
3. :herb: Create a new branch and check it out.
4. :crystal_ball: Make your changes and commit them locally. Magic happens here!
5. :arrow_heading_up: Push your new branch to your fork. (e.g. `git push username fix-issue-16`).
6. :inbox_tray: Open a Pull Request on github.com from your new branch on your fork to `main` in this repository.
