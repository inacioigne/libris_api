import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_create_user(async_client):

    payload = {
        "name": "testuser",
        "email": "user@mail.com",
        "password": "strongpassword"
    }
    response = await async_client.post(
        "/users/",
        json=payload
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['name'] == payload['name']