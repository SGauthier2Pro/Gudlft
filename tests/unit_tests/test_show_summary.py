import tests.conftest
from tests.conftest import client, mock_clubs, mock_competitions
import server


class TestShowSummary:

    def test_show_summary_route_with_valid_email(self,
                                                 client,
                                                 mock_clubs,
                                                 mock_competitions):
        clubs = mock_clubs
        competitions = mock_competitions

        response = client.post(
            '/show_summary',
            data=dict(email=clubs[0]['email']),
            follow_redirects=True
        )
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find(f"<h2>Welcome, {clubs[0]['email']} <//h2>") == -1
        assert data.find(f"Points Available : {clubs[0]['points']}") == -1
        for competition in competitions:
            assert data.find(f"{competition['name']}<br />"
                             f"Date: {competition['date']}</br> "
                             f"Number of Places: "
                             f"{competition['numberOfPlaces']}"
                             f"") == -1

    def test_show_summary_route_with_unknown_email(self, client):
        response = client.post(
            '/show_summary',
            data=dict(email='unknown@email.net'),
            follow_redirects=True
        )
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("This email is not registered !")
