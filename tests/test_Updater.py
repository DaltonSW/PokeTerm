from unittest.mock import patch
import Updater

@patch('Updater.requests.get')
def test_GetLatestVersionFromGithub_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.url = 'https://github.com/DaltonSW/PokeTerm/releases/latest/0.0.1'

    version = Updater.GetLatestVersionFromGithub()
    assert version == '0.0.1'
    mock_get.assert_called_once_with('https://github.com/DaltonSW/PokeTerm/releases/latest')


@patch('Updater.requests.get')
def test_GetLatestVersionFromGithub_failure(mock_get):
    mock_get.return_value.status_code = 404
    mock_get.return_value.url = 'https://github.com/DaltonSW/PokeTerm/releases/latest/0.0.1'

    version = Updater.GetLatestVersionFromGithub()
    assert version is None
    mock_get.assert_called_once_with('https://github.com/DaltonSW/PokeTerm/releases/latest')

@patch('Updater.APP_VERSION', '0.1.0')
def test_IsNewerVersion():
    assert Updater.IsNewerVersion('0.0.0') is False
    assert Updater.IsNewerVersion('0.0.1') is False
    assert Updater.IsNewerVersion('0.1.1') is True
    assert Updater.IsNewerVersion('1.0.0') is True
    assert Updater.IsNewerVersion('0.2.0') is True
    assert Updater.IsNewerVersion('0.1.0') is False
