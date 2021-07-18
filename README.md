# pytest-motor

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
