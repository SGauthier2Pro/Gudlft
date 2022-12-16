import pytest
import server


@pytest.fixture
def client():
    app = server.app
    app.testing = True

    with app.test_client() as client:
        yield client


'''def clubs(mocker):
    mocker.patch('server.load_clubs',
                 return_value=[
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
                 )
    return server.load_clubs()


def competitions(mocker):
    mocker.patch('server.load_competitions',
                 return_value=[
                     {
                         "name": "Spring Festival",
                         "date": "2020-03-27 10:00:00",
                         "numberOfPlaces": "25"
                     },
                     {
                         "name": "Fall Classic",
                         "date": "2020-10-22 13:30:00",
                         "numberOfPlaces": "13"
                     }
                 ]
                 )

    return server.load_competitions()'''
