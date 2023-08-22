from fastapi.testclient import TestClient
from core.config import settings


def test_home(client: TestClient) -> None:

    # ignore spec_id key
    response = client.get(f'{settings.API_V1_STR}/')

    # value_error: missing spec_id
    assert response.status_code == 200
    json_response = response.json()
    assert json_response == {"ping": "pong"}
