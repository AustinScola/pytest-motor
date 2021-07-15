# Contributing to `pytest-motor` 

Hello friend! Here are some guidelines on how to contribute to `pytest-motor`.

## Steps

1. If you do not have a fork of `pytest-motor`, then [create a fork][1] and [clone it][2].
2. Create a branch.
3. Create changes and make sure all code quality scripts pass.
4. Commits your changes.
5. Create a [pull request from your fork][3].

## Scripts

`pytest-motor` has a number of bash scripts in the `scripts` directory. The scripts check the
functionality and quality of the code.

All of the scripts first set up a virtual environment with the appropriate requirements. The first
time that a script is run it may be slow for this reason. Subsequent runs will re-use the venv if
dependencies have not changed.

Here is a description of what each script does:

| Script          | Description                                     |
|-----------------|-------------------------------------------------|
| `all.sh`        | Formats, lints, runs coverage, and type checks. |
| `build.sh`      | Builds distributions using `setuptools`.        |
| `coverage.sh`   | Checks test coverage using `pytest-cov`.        |
| `format.sh`     | Formats code using `yapf` then `isort`.         |
| `lint.sh`       | Lints code using `pylint`.                      |
| `test.sh`       | Tests code using `pytest`.                      |
| `type_check.sh` | Type checks code using `mypy`.                  |

[1]: https://docs.github.com/en/get-started/quickstart/fork-a-repo#forking-a-repository
[2]: https://docs.github.com/en/get-started/quickstart/fork-a-repo#cloning-your-forked-repository
[3]: https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork
