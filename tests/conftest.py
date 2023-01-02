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
                         "points": "16",
                         "booked":
                             {
                                 "Test competition 2": 5,
                                 "Test competition 1": 1
                             }

                     },
                     {
                         "name": "club 2",
                         "email": "admin@club2.com",
                         "points": "4",
                         "booked": {}
                     },
                     {
                         "name": "club 3",
                         "email": "kate@club3.uk",
                         "points": "12",
                         "booked": {}
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


@pytest.fixture
def mock_clubs_json_file(tmpdir):
    json_content = (
        '{"clubs": [\n'
        '   {\n'
        '       "name": "Club 1",\n'
        '       "email": "club1@test.net",\n'
        '       "points": "13",\n'
        '       "booked": {}\n'
        '   }\n'
        ']}\n'
    )
    temp_clubs_file = tmpdir.join('temp-clubs_file.json')
    temp_clubs_file.write_text(json_content, encoding='utf-8')
    yield temp_clubs_file


@pytest.fixture
def mock_competitions_json_file(tmpdir):
    json_content = (
        '{"competitions": [\n'
        '   {\n'
        '       "name": "Competition 1",\n'
        '       "date": "2023-10-22 13:30:00",\n'
        '       "numberOfPlaces": "13"\n'
        '   }\n'
        ']}\n'
    )
    temp_competitions_file = tmpdir.join('temp-competitions_file.json')
    temp_competitions_file.write_text(json_content, encoding='utf-8')
    yield temp_competitions_file

