import pytest
from fastapi import status
import random
import string

@pytest.mark.asyncio
async def test_create_user(async_client):
    
    letras = string.ascii_lowercase + string.digits
    name = ''.join(random.choices(letras, k=8))

    payload = {
        "name": name,
        "email": f"{name}@mail.com",
        "password": "strongpassword"
    }
    response = await async_client.post(
        "/users/",
        json=payload
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['name'] == payload['name']