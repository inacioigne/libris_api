import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_create_user(async_client):
    response = await async_client.post("/users/")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"message": "User created"}