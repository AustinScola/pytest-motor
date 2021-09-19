# pytest-motor

[![PyPI version](https://img.shields.io/pypi/v/pytest-motor.svg)](https://pypi.org/project/pytest-motor/)
[![PyPI status](https://img.shields.io/pypi/status/pytest-motor.svg)](https://pypi.python.org/pypi/pytest-motor/)
[![codecov](https://codecov.io/gh/AustinScola/pytest-motor/branch/master/graph/badge.svg)](https://codecov.io/gh/AustinScola/pytest-motor)
![https://github.com/AustinScola/pytest-motor/actions/workflows/main.yaml](https://github.com/AustinScola/pytest-motor/actions/workflows/main.yaml/badge.svg)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pytest-motor.svg)](https://pypi.python.org/pypi/pytest-motor/)
[![Code style](https://img.shields.io/badge/code%20style-yapf-blue.svg)](https://github.com/google/yapf)


A [pytest][1] plugin for [Motor][2], the non-blocking MongoDB driver.

## Installation

To install `pytest-motor`, run:

```bash
pip install pytest-motor
```

## Example

```python3
from motor.motor_asyncio import AsyncIOMotorClient
import pytest


@pytest.mark.asyncio
async def test_using_motor_client(motor_client: AsyncIOMotorClient) -> None:
    """This test has access to a Motor client."""
    await motor_client.server_info()
```

## How it works

When a test session runs, `pytest-motor` checks that the mongod binary is present in the
`.mongod` subdirectory of the pytest root path. If it is not preset, it will be downloaded. This
means that the first run make take some time. Subsequent runs will be faster.

Each test function uses a new `motor_client` and database. (This may change in the future.)

## Limitations

`pytest-motor` currently supports:

- Ubuntu 16.04*, 18.04, and 20.04
- Debian 9.2* and 10.0*
- MacOS
- Windows

*NOT tested.

If you would like support for another system, please [make a GitHub Issue][3]. Contributions are
welcome!

[1]: https://docs.pytest.org/en/latest/
[2]: https://github.com/mongodb/motor/
[3]: https://github.com/AustinScola/pytest-motor/issues/new
