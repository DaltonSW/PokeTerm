from unittest.mock import patch
from PokeTerm.Updater import (
    GetLatestVersionFromGithub,
    IsNewerVersion
)


class TestUpdater:
    @patch('PokeTerm.Updater.requests.get')
    def test_GetLatestVersionFromGithub_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.url = 'https://github.com/DaltonSW/PokeTerm/releases/latest/0.0.1'

        version = GetLatestVersionFromGithub()
        assert version == '0.0.1'
        mock_get.assert_called_once_with('https://github.com/DaltonSW/PokeTerm/releases/latest')

    @patch('PokeTerm.Updater.requests.get')
    def test_GetLatestVersionFromGithub_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.url = 'https://github.com/DaltonSW/PokeTerm/releases/latest/0.0.1'

        version = GetLatestVersionFromGithub()
        assert version is None
        mock_get.assert_called_once_with('https://github.com/DaltonSW/PokeTerm/releases/latest')

    @patch('PokeTerm.Updater.APP_VERSION', '0.1.0')
    def test_IsNewerVersion(self):
        assert IsNewerVersion('0.0.0') is False
        assert IsNewerVersion('0.0.1') is False
        assert IsNewerVersion('0.1.1') is True
        assert IsNewerVersion('1.0.0') is True
        assert IsNewerVersion('0.2.0') is True
        assert IsNewerVersion('0.1.0') is False
