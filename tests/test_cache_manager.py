import pytest
from poketerm.utils.caching import CacheManager


class TestCacheManager:
    @pytest.fixture
    def clean_cache_manager(self):
        saved_mappings = CacheManager.resource_mappings.copy()
        CacheManager.resource_mappings = {}

        yield

        CacheManager.resource_mappings = saved_mappings

    def test_add_name_to_ID_mapping(self, clean_cache_manager):
        test_key = "type"
        test_name = "normal"
        test_ID = 1
        bad_name = "meh"

        CacheManager.add_name_to_ID_mapping(test_key, test_name, test_ID)

        assert CacheManager.resource_mappings.get(test_key) is not None
        assert (
            CacheManager.resource_mappings.get(test_key).NAME_TO_ID.get(test_name)
            == test_ID
        )
        assert (
            CacheManager.resource_mappings.get(test_key).NAME_TO_ID.get(bad_name)
            is None
        )

    def test_add_ID_to_data_mapping(self, clean_cache_manager):
        test_key = "type"
        test_ID = 1
        test_data = "Data"
        bad_ID = -1

        CacheManager.add_ID_to_data_mapping(test_key, test_ID, test_data)

        assert CacheManager.resource_mappings.get(test_key) is not None
        assert (
            CacheManager.resource_mappings.get(test_key).ID_TO_DATA.get(test_ID)
            == test_data
        )
        assert (
            CacheManager.resource_mappings.get(test_key).ID_TO_DATA.get(bad_ID) is None
        )

    def test_get_ID_from_name(self, clean_cache_manager):
        test_key = "type"
        test_name = "normal"
        test_ID = 1
        bad_name = "meh"

        CacheManager.add_name_to_ID_mapping(test_key, test_name, test_ID)

        assert CacheManager.get_ID_from_name(test_key, test_name) == test_ID
        assert CacheManager.get_ID_from_name(test_key, bad_name) is None

    def test_get_data_from_ID(self, clean_cache_manager):
        test_key = "type"
        test_ID = 1
        test_data = "Data"
        bad_ID = -1

        CacheManager.add_ID_to_data_mapping(test_key, test_ID, test_data)

        assert CacheManager.get_data_from_ID(test_key, test_ID) == test_data
        assert CacheManager.get_data_from_ID(test_key, bad_ID) is None

    def test_get_data_from_name(self, clean_cache_manager):
        test_key = "type"
        test_ID = 1
        test_name = "normal"
        test_data = "Data"
        bad_name = "meh"

        CacheManager.add_name_to_ID_mapping(test_key, test_name, test_ID)
        CacheManager.add_ID_to_data_mapping(test_key, test_ID, test_data)

        assert CacheManager.get_data_from_name(test_key, test_name) == test_data
        assert CacheManager.get_data_from_name(test_key, bad_name) is None
