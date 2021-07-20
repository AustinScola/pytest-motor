# pytest-motor

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

1. Every pytest session you start, `pytest-motor` checks if you have the mongod binary at pytest rootpath/.mongod.

2. If you don't have one, plugin will download and unpack the binary automatically. This, of course, will slow down the first launch, but subsequent runs will be significantly faster.

3. Every function you run will have a separate database connection. MongoDB itself remains clean.

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
