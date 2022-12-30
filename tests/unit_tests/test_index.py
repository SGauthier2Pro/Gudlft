import tests.conftest
from tests.conftest import client, mock_clubs, mock_competitions
import server


class TestIndex:
    def test_index_route_should_status_code_ok(self, client):
        response = client.get('/')
        assert response.status_code == 200
