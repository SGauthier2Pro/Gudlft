from server import InvalidLoadFile, load_clubs
import pytest


class TestLoadClubsFunction:

    def test_missing_clubs_file(self):
        with pytest.raises(InvalidLoadFile):
            load_clubs('invalid-club-file.json')

    def test_invalid_content_clubs_file(self, tmpdir):
        json_content = (
            'dklsjfghkldsfjgh\n'
        )
        temp_clubs_file = tmpdir.join('temp-clubs_file.json')
        temp_clubs_file.write_text(json_content, encoding='utf-8')
        with pytest.raises(InvalidLoadFile):
            load_clubs(temp_clubs_file.strpath)

    def test_empty_clubs_file(self, tmpdir):
        json_content = ''
        temp_clubs_file = tmpdir.join('temp-clubs_file.json')
        temp_clubs_file.write_text(json_content, encoding='utf-8')
        with pytest.raises(InvalidLoadFile):
            load_clubs(temp_clubs_file.strpath)

    def test_valid_clubs_file(self, tmpdir):
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
        parsed_clubs_file = load_clubs(temp_clubs_file.strpath)
        assert parsed_clubs_file[0]['name'] == 'Club 1'
        assert parsed_clubs_file[0]['points'] == '13'

