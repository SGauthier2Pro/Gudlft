import tests.conftest
from tests.conftest import client, mock_clubs, mock_competitions
import server


class TestPurchasePlaces:

    def test_purchase_places_with_club_competition_required_places(
            self,
            client,
            mock_clubs,
            mock_competitions
    ):
        competitions = mock_competitions
        competition = competitions[0]['name']
        clubs = mock_clubs
        club = clubs[0]['name']
        required_places = '10'

        competition_places_rest = \
            int(competitions[0]['numberOfPlaces']) - int(required_places)

        club_points_left = int(clubs[0]['points']) - int(required_places)

        response = client.post('/purchase_places',
                               data=dict(places=required_places,
                                         club=club,
                                         competition=competition),
                               follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()

        assert data.find("Great-booking complete!") != -1
        assert data.find(f"{competition}<br>\n            "
                         f"Date: {competitions[0]['date']}<br>\n            "
                         f"Number of Places: {competition_places_rest}") != -1
        assert data.find(f"Points available: {club_points_left}") != -1

    def test_purchase_places_with_unknown_club(self,
                                               client,
                                               mock_competitions):
        competitions = mock_competitions
        competition = competitions[0]['name']
        club = 'wrong club'
        required_places = '10'

        response = client.post('/purchase_places',
                               data=dict(places=required_places,
                                         club=club,
                                         competition=competition),
                               follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()

        assert data.find("Club does not existes !") != -1

    def test_purchase_places_with_unknown_competition(self,
                                                      client,
                                                      mock_clubs):
        competition = 'wrong competition'
        clubs = mock_clubs
        club = clubs[0]['name']
        required_places = '10'

        response = client.post('/purchase_places',
                               data=dict(places=required_places,
                                         club=club,
                                         competition=competition),
                               follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()

        assert data.find("Competition does not existes !") != -1

    def test_purchase_places_with_more_than_twelve_required_places(
            self,
            client,
            mock_clubs,
            mock_competitions
    ):
        competitions = mock_competitions
        competition = competitions[0]['name']
        clubs = mock_clubs
        club = clubs[0]['name']
        required_places = '12'

        response = client.post('/purchase_places',
                               data=dict(places=required_places,
                                         club=club,
                                         competition=competition),
                               follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()

        assert data.find("You can not purchase "
                         "more than 12 places per event!") != -1

    def test_purchase_places_with_not_enough_available_points(
            self,
            client,
            mock_clubs,
            mock_competitions
    ):
        competitions = mock_competitions
        competition = competitions[0]['name']
        clubs = mock_clubs
        club = clubs[1]['name']
        required_places = '10'

        response = client.post('/purchase_places',
                               data=dict(places=required_places,
                                         club=club,
                                         competition=competition),
                               follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()

        assert data.find("Not enough available points!") != -1

    def test_purchase_places_with_not_enough_available_places(
            self,
            client,
            mock_clubs,
            mock_competitions
    ):
        competitions = mock_competitions
        competition = competitions[2]['name']
        clubs = mock_clubs
        club = clubs[2]['name']
        required_places = '10'

        response = client.post('/purchase_places',
                               data=dict(places=required_places,
                                         club=club,
                                         competition=competition),
                               follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()

        assert data.find("Not enough available places!") != -1

    def test_purchase_places_with_past_competition(self,
                                                   client,
                                                   mock_clubs,
                                                   mock_competitions):
        competitions = mock_competitions
        competition = competitions[1]['name']
        clubs = mock_clubs
        club = clubs[0]['name']
        required_places = '10'

        response = client.post('/purchase_places',
                               data=dict(places=required_places,
                                         club=club,
                                         competition=competition),
                               follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()

        assert data.find("You can not purchase "
                         "places for a past competition") != -1

    def test_purchase_places_with_negative_required_places(
            self,
            client,
            mock_clubs,
            mock_competitions
    ):
        competitions = mock_competitions
        competition = competitions[1]['name']
        clubs = mock_clubs
        club = clubs[0]['name']
        required_places = '-2'

        response = client.post('/purchase_places',
                               data=dict(places=required_places,
                                         club=club,
                                         competition=competition),
                               follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()

        assert data.find("You can not purchase a "
                         "negative number of place !") != -1

    def test_purchase_places_with_zero_required_places(
            self,
            client,
            mock_clubs,
            mock_competitions
    ):
        competitions = mock_competitions
        competition = competitions[1]['name']
        clubs = mock_clubs
        club = clubs[0]['name']
        required_places = '0'

        response = client.post('/purchase_places',
                               data=dict(places=required_places,
                                         club=club,
                                         competition=competition),
                               follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()

        assert data.find("You have not booked any place !") != -1

    def test_purchase_places_with_empty_required_places(
            self,
            client,
            mock_clubs,
            mock_competitions
    ):
        competitions = mock_competitions
        competition = competitions[1]['name']
        clubs = mock_clubs
        club = clubs[0]['name']
        required_places = ''

        response = client.post('/purchase_places',
                               data=dict(places=required_places,
                                         club=club,
                                         competition=competition),
                               follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()

        assert data.find("You have to enter a number of place !") != -1
