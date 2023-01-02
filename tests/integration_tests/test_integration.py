import server


class TestIntegration:

    def setup_method(self):
        self.clubs = []
        self.competitions = []
        self.club = ''
        self.competition = ''

    def test_index_route(self, client):
        response = client.get('/')
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("<h1>Welcome to the "
                         "GUDLFT Registration Portal!<//h1>")

    def test_boardpoints_route(self, client, mock_clubs_json_file):

        server.clubs = server.load_clubs(mock_clubs_json_file.strpath)
        self.clubs = server.clubs

        response = client.get('/boardpoints')
        data = response.data.decode()
        assert data.find("<h2>Boardpoints of Clubs </h2>") != -1
        assert data.find("<td>Club Name</td>") != -1
        assert data.find("<td>Number of available points</td>") != -1
        for club in self.clubs:
            assert data.find(f"<td>{club['name']}</td>") != -1
            assert data.find(f"<td>{club['points']}</td>") != -1

    def test_purchasing_routine(self,
                                client,
                                mock_clubs_json_file,
                                mock_competitions_json_file):

        server.clubs = server.load_clubs(mock_clubs_json_file.strpath)
        self.clubs = server.clubs
        server.competitions = server.load_competitions(
            mock_competitions_json_file.strpath)
        self.competitions = server.competitions

        # select  the club for test
        self.club = self.clubs[0]['name']

        response = client.post(
            '/show_summary',
            data=dict(email=self.clubs[0]['email']),
            follow_redirects=True
        )

        # check if the redirected page show_summary is loaded
        assert response.status_code == 200

        # check if the page contains what we expect
        data = response.data.decode()
        assert data.find(f"<h2>Welcome, {self.clubs[0]['email']} </h2>") != -1
        assert data.find(f"Points available: {self.clubs[0]['points']}") != -1
        for competition in self.competitions:
            assert data.find(f"{competition['name']}<br>") != -1
            assert data.find(f"Date: {competition['date']}<br>") != -1
            assert data.find(f"Number of Places: "
                             f"{competition['numberOfPlaces']}") != -1

        # select the competition to target for purchasing places
        self.competition = self.competitions[0]['name']

        # start the booking process for selected competition by
        # the selected club
        response = client.get(f'/book/{self.competition}/{self.club}')

        # check if the redirected page book is loaded
        assert response.status_code == 200

        # check if the page contains what we expected
        data = response.data.decode()
        assert data.find(f"<h2>{self.competition}</h2>") != -1
        assert data.find(f"Places "
                         f"available: {self.competitions[0]['numberOfPlaces']}"
                         ) != -1

        # posting of the number of places we want to purchase
        required_places = '10'

        competition_places_rest = \
            int(self.competitions[0]['numberOfPlaces']) - int(required_places)

        club_points_left = int(self.clubs[0]['points']) - int(required_places)

        response = client.post('/purchase_places',
                               data=dict(places=required_places,
                                         club=self.club,
                                         competition=self.competition),
                               follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()

        assert data.find("Great-booking complete!") != -1
        assert data.find(f"{self.competition}<br>\n            "
                         f"Date: {self.competitions[0]['date']}<br>\n"
                         f"            "
                         f"Number of Places: {competition_places_rest}") != -1
        assert data.find(f"Points available: {club_points_left}") != -1
