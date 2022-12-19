import pytest
import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    client = server.app.test_client()
    return client


@pytest.fixture
def mock_clubs(mocker):
    clubs = [
                     {
                         "name": "club 1",
                         "email": "john@club1.net",
                         "points": "13"
                     },
                     {
                         "name": "club 2",
                         "email": "admin@club2.com",
                         "points": "4"
                     },
                     {
                         "name": "club 3",
                         "email": "kate@club3uk",
                         "points": "12"
                     }
                 ]
    mocked_clubs = mocker.patch.object(server, 'clubs', clubs)
    yield mocked_clubs


@pytest.fixture
def mock_competitions(mocker):
    competitions = [
                     {
                         "name": "Test competition 1",
                         "date": "2023-03-27 10:00:00",
                         "numberOfPlaces": "25"
                     },
                     {
                         "name": "Test competition 2",
                         "date": "2020-10-22 13:30:00",
                         "numberOfPlaces": "13"
                     },
                     {
                         "name": "Test competition 3",
                         "date": "2023-10-22 13:30:00",
                         "numberOfPlaces": "3"
                     }
                 ]
    mocked_competitions = mocker.patch.object(server,
                                              'competitions',
                                              competitions)
    yield mocked_competitions
