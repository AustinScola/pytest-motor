# pytest-motor

A [pytest][1] plugin for motor, the non-blocking MongoDB driver.

## Example

``` Python3
from motor.motor_asyncio import AsyncIOMotorClient
import pytest


@pytest.mark.asyncio
async def test_using_motor_client(motor_client: AsyncIOMotorClient) -> None:
    """This test has access to a Motor client."""
    await motor_client.server_info()
```

[1]: https://docs.pytest.org/en/latest/
