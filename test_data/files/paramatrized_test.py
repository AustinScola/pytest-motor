"""A test file with a paramatrized test."""
from typing import Any, Dict

import pytest
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase


@pytest.mark.asyncio
# yapf: disable
@pytest.mark.parametrize('document', [
    ({}),
    ({'foo': 'bar'}),
    ({'wibble': 'wobble'}),
])
# yapf: enable
async def test_with_parametrization(motor_client: AsyncIOMotorClient, document: Dict[str,
                                                                                     Any]) -> None:
    """This test is parametrized."""
    database: AsyncIOMotorDatabase = motor_client['database']
    collection: AsyncIOMotorCollection = database['collection']

    await collection.insert_one(document)

    assert (await collection.count_documents({})) == 1
