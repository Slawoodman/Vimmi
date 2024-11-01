from assets.scripts.script import upload_movies, InvalidJSONError
from unittest.mock import mock_open, patch
import json
import pytest


class TestScriptsFile:
    @pytest.fixture
    def valid_json_data(self):
        return {
            "items": [
                {
                    "title": "The Shawshank Redemption",
                    "year": "1994",
                    "imDbRating": "9.3",
                },
                {"title": "The Godfather", "year": "1972", "imDbRating": "9.2"},
            ]
        }

    def test_file_upload(self):
        with pytest.raises(FileNotFoundError):
            upload_movies("NoFile")

    def test_invalid_json_load(self):
        with patch("builtins.open", mock_open(read_data="{Invalid JSON}")):
            with pytest.raises(InvalidJSONError) as excinfo:
                upload_movies("invalid_json_load.json")

            assert (
                str(excinfo.value)
                == "Error: The file 'invalid_json_load.json' is not a valid JSON file."
            )

    def test_successful_upload(self, valid_json_data):
        with patch("builtins.open", mock_open(read_data=json.dumps(valid_json_data))):
            with patch("sqlite3.connect") as mock_connect:
                mock_conn = mock_connect.return_value
                mock_cursor = mock_conn.cursor.return_value

                with patch(
                    "assets.scripts.script.connect_to_db",
                    return_value=(mock_conn, mock_cursor),
                ):
                    upload_movies("dummy_path.json")
                    assert mock_cursor.execute.call_count > 0

                mock_conn.commit.assert_called_once()
                mock_conn.close.assert_called_once()
