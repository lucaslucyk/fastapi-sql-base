from fastapi import status
from fastapi.testclient import TestClient
from schemas.users import UserCreate, UserUpdate, User
from core.config import settings


def test_users_list(client: TestClient) -> None:
    """Test users list endpoint. Must be an empty list.

    Args:
        client (TestClient): App Client
    """

    response = client.get(f'{settings.API_V1_STR}/users/')
    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == []


def test_users_bad_create(client: TestClient) -> None:
    """Test user bad create with bad format

    Args:
        client (TestClient): App Client
    """
    
    response = client.post(
        url=f'{settings.API_V1_STR}/users/',
        json={"bad-username": "testing"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_users_create(client: TestClient) -> None:
    """Test user create

    Args:
        client (TestClient): App Client
    """
    
    response = client.post(
        url=f'{settings.API_V1_STR}/users/',
        json=UserCreate(username="testing").model_dump()
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_users_list_content(client: TestClient) -> None:
    """Test users list with no empty content

    Args:
        client (TestClient): App Client
    """

    response = client.get(f'{settings.API_V1_STR}/users/')
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_user_get(client: TestClient) -> None:
    """Test get an user

    Args:
        client (TestClient): App Client
    """

    response = client.get(f'{settings.API_V1_STR}/users/1/')
    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert User(**json_response).model_dump() == json_response


def test_user_bad_get(client: TestClient) -> None:
    """Test get a non-existent user

    Args:
        client (TestClient): App Client
    """

    response = client.get(f'{settings.API_V1_STR}/users/2/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_user_update(client: TestClient) -> None:
    """Test update a current user

    Args:
        client (TestClient): App Client
    """

    response = client.patch(
        url=f'{settings.API_V1_STR}/users/1/',
        json=UserUpdate(username="testing-update").model_dump()
    )
    assert response.status_code == status.HTTP_200_OK


def test_user_bad_update(client: TestClient) -> None:
    """Test update a non-existent user

    Args:
        client (TestClient): App Client
    """

    response = client.patch(
        url=f'{settings.API_V1_STR}/users/2/',
        # json={"bad-username": "testing"}
        json=UserUpdate(username="testing-update-2").model_dump()
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_user_bad_delete(client: TestClient) -> None:
    """Test delete a non-existent user

    Args:
        client (TestClient): App Client
    """

    response = client.delete(f'{settings.API_V1_STR}/users/2/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_user_delete(client: TestClient) -> None:
    """Test delete an existent user

    Args:
        client (TestClient): App Client
    """
    
    response = client.delete(f'{settings.API_V1_STR}/users/1/')
    assert response.status_code == status.HTTP_200_OK