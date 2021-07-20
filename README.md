# pytest-motor

[![PyPI version](https://img.shields.io/pypi/v/pytest-motor.svg)](https://pypi.org/project/pytest-motor/)
[![PyPI status](https://img.shields.io/pypi/status/pytest-motor.svg)](https://pypi.python.org/pypi/pytest-motor/)
[![codecov](https://codecov.io/gh/AustinScola/pytest-motor/branch/master/graph/badge.svg)](https://codecov.io/gh/AustinScola/pytest-motor)
![https://github.com/AustinScola/pytest-motor/actions/workflows/python.yaml](https://github.com/AustinScola/pytest-motor/actions/workflows/python.yaml/badge.svg)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pytest-motor.svg)](https://pypi.python.org/pypi/pytest-motor/)
[![Code style](https://img.shields.io/badge/code%20style-yapf-blue.svg)](https://github.com/google/yapf)


A [pytest][1] plugin for [Motor][2], the non-blocking MongoDB driver.

## Example

``` Python3
from motor.motor_asyncio import AsyncIOMotorClient
import pytest


@pytest.mark.asyncio
async def test_using_motor_client(motor_client: AsyncIOMotorClient) -> None:
    """This test has access to a Motor client."""
    await motor_client.server_info()
```

## Limitations

`pytest-motor` currently only supports Ubuntu 18.04 and MacOS. Windows support is being worked on.
If you would like support for another system, please [make a GitHub Issue][3]. Contributions are
welcome!

[1]: https://docs.pytest.org/en/latest/
[2]: https://github.com/mongodb/motor/
[3]: https://github.com/AustinScola/pytest-motor/issues/new
