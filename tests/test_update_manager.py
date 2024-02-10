from unittest.mock import patch, Mock
from poketerm.utils import updater


class TestUpdateManager:
    @patch("requests.get")
    def test_get_latest_version_from_github(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = "https://github.com/DaltonSW/PokeTerm/releases/latest/1.1.1"
        mock_get.return_value = mock_response

        version = updater.get_latest_version_from_github()
        assert version == "1.1.1"

    @patch("poketerm.config.APP_VERSION", "1.2.3")
    def test_is_newer_version(self):
        assert updater.is_newer_version("1.2.4")
        assert updater.is_newer_version("2.0.0")
        assert updater.is_newer_version("1.3.2")
        assert updater.is_newer_version("1.2.3") is False
        assert updater.is_newer_version("0.0.0") is False
        assert updater.is_newer_version("0.3.4") is False
        assert updater.is_newer_version("1.2.2") is False
