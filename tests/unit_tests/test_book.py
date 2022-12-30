import tests.conftest
from tests.conftest import client, mock_clubs, mock_competitions
import server


class TestBook:

    def test_book_route_with_good_competition_and_good_club(self,
                                                            client,
                                                            mock_clubs,
                                                            mock_competitions):
        clubs = mock_clubs
        club = clubs[0]['name']
        competitions = mock_competitions
        competition = competitions[0]['name']

        response = client.get(f'/book/{competition}/{club}')
        assert response.status_code == 200

    def test_book_route_with_unknown_competition_and_good_club(self,
                                                               client,
                                                               mock_clubs):
        clubs = mock_clubs
        club = clubs[0]['name']
        competition = 'wrong competition'

        response = client.get(f'/book/{competition}/{club}')
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("Something went wrong-please try again") != -1

    def test_book_route_with_good_competition_and_unknown_club(
            self,
            client,
            mock_competitions
    ):
        club = 'wrong club'
        competitions = mock_competitions
        competition = competitions[0]['name']

        response = client.get(f'/book/{competition}/{club}')
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("Something went wrong-please try again") != -1

    def test_book_route_with_unknown_competition_and_unknown_club(self,
                                                                  client):
        club = 'wrong club'
        competition = 'wrong competition'

        response = client.get(f'/book/{competition}/{club}')
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("Something went wrong-please try again") != -1

    def test_book_route_with_past_competition_and_valid_club(
            self,
            client,
            mock_clubs,
            mock_competitions
    ):
        competitions = mock_competitions
        competition = competitions[1]['name']
        clubs = mock_clubs
        club = clubs[0]['name']

        response = client.get(f'/book/{competition}/{club}')
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("You can not book "
                         "places for a past competition") != -1