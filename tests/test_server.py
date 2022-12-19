import tests.conftest
from tests.conftest import client, mock_clubs, mock_competitions
import server
from server import load_clubs, load_competitions


class TestServer:
    def test_index_route_should_status_code_ok(self, client):
        response = client.get('/')
        assert response.status_code == 200

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

    def test_book_route_with_good_competition_and_good_club(self, client):
        clubs = load_clubs()
        club = clubs[0]['name']
        competitions = load_competitions()
        competition = competitions[0]['name']

        response = client.get(f'/book/{competition}/{club}')
        assert response.status_code == 200

    def test_book_route_with_unknown_competition_and_good_club(self, client):
        clubs = load_clubs()
        club = clubs[0]['name']
        competition = 'wrong competition'

        response = client.get(f'/book/{competition}/{club}')
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("Something went wrong-please try again") != -1

    def test_book_route_with_good_competition_and_unknown_club(self, client):
        club = 'wrong club'
        competitions = load_competitions()
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

    def test_purchase_places_with_club_competition_required_places(self,
                                                                   client):
        competitions = load_competitions()
        competition = competitions[0]['name']
        clubs = load_clubs()
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

    def test_purchase_places_with_unknown_club(self, client):
        competitions = load_competitions()
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

    def test_purchase_places_with_unknown_competition(self, client):
        competition = 'wrong competition'
        clubs = load_clubs()
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

    def test_purchase_places_with_more_than_twelve_required_places(self,
                                                                   client):
        competitions = load_competitions()
        competition = competitions[0]['name']
        clubs = load_clubs()
        club = clubs[0]['name']
        required_places = '15'

        response = client.post('/purchase_places',
                               data=dict(places=required_places,
                                         club=club,
                                         competition=competition),
                               follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()

        assert data.find("You can not purchase more than 12 places!") != -1

    def test_purchase_places_with_not_enough_available_points(self,
                                                              client):
        competitions = load_competitions()
        competition = competitions[0]['name']
        clubs = load_clubs()
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

    def test_purchase_places_with_not_enough_available_places(self,
                                                              client):
        competitions = load_competitions()
        competition = competitions[0]['name']
        clubs = load_clubs()
        club = clubs[1]['name']
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
                                                   client):
        competitions = load_competitions()
        competition = competitions[1]['name']
        clubs = load_clubs()
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

    def test_logout(self, client):
        response = client.get('/logout',
                              follow_redirects=True)
        assert response.status_code == 200
