# import pytest
#
#
# @pytest.mark.asyncio
# async def test_sign_new_user(default_client) -> None:
#     payload = {"email": "testuser@packt.com", "password": "testpassword"}
#
#     headers = {"accept": "application/json", "Content-Type": "application/json"}
#
#     test_response = {"message": "User created successfully"}
#
#     async with default_client as client:
#         response = await client.post("/user/signup", json=payload, headers=headers)
#         assert response.status_code == 200
#         assert response.json() == test_response


import pytest


@pytest.mark.asyncio
async def test_sign_new_user(default_client) -> None:
    payload = {"email": "testuser@packt.com", "password": "testpassword"}

    headers = {"accept": "application/json", "Content-Type": "application/json"}

    test_response = {"message": "User created successfully"}

    response = await default_client.post("/user/signup", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response
