"""A test file with a multiple tests with independent Motor clients."""
import pytest
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase


@pytest.mark.asyncio
async def test_one(motor_client: AsyncIOMotorClient) -> None:
    """This test reads and writes some data, it should be independent of the other test."""
    database: AsyncIOMotorDatabase = motor_client['database']
    collection: AsyncIOMotorCollection = database['collection']

    await collection.insert_one({})

    assert (await collection.count_documents({})) == 1


@pytest.mark.asyncio
async def test_two(motor_client: AsyncIOMotorClient) -> None:
    """This test also reads and writes some data, and it should be independent of the other test."""
    database: AsyncIOMotorDatabase = motor_client['database']
    collection: AsyncIOMotorCollection = database['collection']

    await collection.insert_one({})

    assert (await collection.count_documents({})) == 1
