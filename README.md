# pytest-motor

[![PyPI version](https://img.shields.io/pypi/v/pytest-motor.svg)](https://pypi.org/project/pytest-motor/)
[![PyPI status](https://img.shields.io/pypi/status/pytest-motor.svg)](https://pypi.python.org/pypi/pytest-motor/)
[![codecov](https://codecov.io/gh/AustinScola/pytest-motor/branch/master/graph/badge.svg)](https://codecov.io/gh/AustinScola/pytest-motor)
![https://github.com/AustinScola/pytest-motor/actions/workflows/python.yaml](https://github.com/AustinScola/pytest-motor/actions/workflows/python.yaml/badge.svg)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pytest-motor.svg)](https://pypi.python.org/pypi/pytest-motor/)
[![Code style](https://img.shields.io/badge/code%20style-yapf-blue.svg)](https://github.com/google/yapf)


A [pytest][1] plugin for [Motor][2], the non-blocking MongoDB driver.

## Installation

To install pytest-motor, simply:

``` bash
pip install pytest-motor
```

This is enough for pytest to pick up pytest-motor.

## Example

``` Python3
from motor.motor_asyncio import AsyncIOMotorClient
import pytest


@pytest.mark.asyncio
async def test_using_motor_client(motor_client: AsyncIOMotorClient) -> None:
    """This test has access to a Motor client."""
    await motor_client.server_info()
```

## How it works

1. Every pytest session you start, `pytest-motor` checks if you have mongod binary at pytest rootpath/.mongod.

2. If you don't have one, plugin will download and unpack the binary automatically. This, of course, will slow down the first launch, but subsequent runs will be significantly faster.

3. Every function you run will have separate database connection. MongoDB itself remains clean.

## Limitations

`pytest-motor` currently supports:

- Ubuntu
  - 16.04*
  - 18.04
  - 20.04
- Debian
  - 9.2*
  - 10.0*
- macOS
- Windows

*none of the contributors use this version, so it is NOT properly tested.

If you would like support for another system, please [make a GitHub Issue][3]. Contributions are
welcome!

[1]: https://docs.pytest.org/en/latest/
[2]: https://github.com/mongodb/motor/
[3]: https://github.com/AustinScola/pytest-motor/issues/new
