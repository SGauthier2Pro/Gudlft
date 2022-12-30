from server import InvalidLoadFile, load_competitions
import pytest


class TestLoadCompetitionsFunction:

    def test_missing_competitions_file(self):
        with pytest.raises(InvalidLoadFile):
            load_competitions('invalid-competition-file.json')

    def test_invalid_content_competitions_file(self, tmpdir):
        json_content = (
            'dklsjfghkldsfjgh\n'
        )
        temp_competitions_file = tmpdir.join('temp-clubs_file.json')
        temp_competitions_file.write_text(json_content, encoding='utf-8')
        with pytest.raises(InvalidLoadFile):
            load_competitions(temp_competitions_file.strpath)

    def test_empty_competitions_file(self, tmpdir):
        json_content = ''
        temp_competitions_file = tmpdir.join('temp-clubs_file.json')
        temp_competitions_file.write_text(json_content, encoding='utf-8')
        with pytest.raises(InvalidLoadFile):
            load_competitions(temp_competitions_file.strpath)

    def test_valid_competitions_file(self, tmpdir):
        json_content = (
            '{"competitions": [\n'
            '   {\n'
            '       "name": "Competition 1",\n'
            '       "date": "2020-10-22 13:30:00",\n'
            '       "numberOfPlaces": "13"\n'
            '   }\n'
            ']}\n'
        )
        temp_competitions_file = tmpdir.join('temp-clubs_file.json')
        temp_competitions_file.write_text(json_content, encoding='utf-8')
        parsed_competitions_file = load_competitions(
            temp_competitions_file.strpath)
        assert parsed_competitions_file[0]['name'] == 'Competition 1'
        assert parsed_competitions_file[0]['numberOfPlaces'] == '13'
