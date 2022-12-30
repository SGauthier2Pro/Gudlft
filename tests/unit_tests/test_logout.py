import tests.conftest
from tests.conftest import client, mock_clubs, mock_competitions
import server


class TestLogout:

    def test_logout(self, client):
        response = client.get('/logout',
                              follow_redirects=True)
        assert response.status_code == 200
