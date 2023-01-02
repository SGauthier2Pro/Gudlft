class TestBoardPoints:
    def test_boardpoints_route_should_status_code_ok(self, client):
        response = client.get('/boardpoints')
        assert response.status_code == 200

    def test_boardpoints_route_should_show_each_club_points(self,
                                                            client,
                                                            mock_clubs):
        clubs = mock_clubs

        response = client.get('/boardpoints')
        data = response.data.decode()
        assert data.find("<h2>Boardpoints of Clubs </h2>") != -1
        assert data.find("<td>Club Name</td>") != -1
        assert data.find("<td>Number of available points</td>") != -1
        for club in clubs:
            assert data.find(f"<td>{club['name']}</td>") != -1
            assert data.find(f"<td>{club['points']}</td>") != -1
