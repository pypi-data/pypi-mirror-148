import json
import unittest
import unittest.mock as mock
from iplkp.cache import IplkpCache
from iplkp.consts import RDAP_LOOKUP_TASK_NAME, GEO_IP_LOOKUP_TASK_NAME

EMPTY_CACHE = {
    RDAP_LOOKUP_TASK_NAME: {},
    GEO_IP_LOOKUP_TASK_NAME: {}
}

FIND_ALL_TEST_CACHE = {
    RDAP_LOOKUP_TASK_NAME: {
        "10.0.0.5": {"data": "some_data"},
        "192.168.1.1": {"data": "some_data"}
    },
    GEO_IP_LOOKUP_TASK_NAME: {
        "10.0.0.5": {"data": "some_data"},
        "8.8.8.8": {"data": "some_data"}
    }
}

class TestCache(unittest.TestCase):
    def setUp(self):
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(EMPTY_CACHE))) as mo:
            self.in_memory_cache = IplkpCache()
          
    def test_init_empty(self):
        expected = EMPTY_CACHE
        result = self.in_memory_cache._init_empty()
        self.assertDictEqual(expected, result, "Expected cache to be empty")

    def test_get_rdap(self):
        ip = "192.168.1.1"
        rdap_results = {ip: {"some_key": "some_value"}}
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(EMPTY_CACHE))) as mo:
            self.in_memory_cache.update({RDAP_LOOKUP_TASK_NAME: rdap_results})
        self.assertTrue(self.in_memory_cache.get_rdap(ip))

    def test_get_ip(self):
        ip = "192.168.1.1"
        ip_results = {ip: {"some_key": "some_value"}}
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(EMPTY_CACHE))) as mo:
            self.in_memory_cache.update({GEO_IP_LOOKUP_TASK_NAME: ip_results})
        self.assertTrue(self.in_memory_cache.get_geo_ip(ip))

    def test_update(self):
        ip = "192.168.1.1"
        data_to_add = EMPTY_CACHE
        data_to_add[RDAP_LOOKUP_TASK_NAME] = {ip: {"status": "rdap data"}}
        data_to_add[GEO_IP_LOOKUP_TASK_NAME] = {ip: {"status": "geo ip data"}}

        self.assertFalse(self.in_memory_cache.get_geo_ip(ip))
        self.assertFalse(self.in_memory_cache.get_rdap(ip))
        
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(EMPTY_CACHE))) as mo:
            self.in_memory_cache.update(data_to_add)
        
        self.assertTrue(self.in_memory_cache.get_geo_ip(ip))
        self.assertTrue(self.in_memory_cache.get_rdap(ip))

    def test_find_all_cache_has_all_data_all_queries(self):
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(EMPTY_CACHE))) as mo:
            self.in_memory_cache.update(FIND_ALL_TEST_CACHE)
        hits, misses = self.in_memory_cache.find_all(["10.0.0.5"])
        expected_hits = {
            RDAP_LOOKUP_TASK_NAME: {"10.0.0.5": {"data": "some_data"}},
            GEO_IP_LOOKUP_TASK_NAME: {"10.0.0.5": {"data": "some_data"}}
        }
        expected_misses = []
        self.assertDictEqual(hits, expected_hits)
        self.assertEqual(misses, expected_misses)

    def test_find_all_cache_has_all_data_just_rdap(self):
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(EMPTY_CACHE))) as mo:
            self.in_memory_cache.update(FIND_ALL_TEST_CACHE)
        hits, misses = self.in_memory_cache.find_all(["10.0.0.5", "192.168.1.1"], just_rdap=True)
        expected_hits = {
            RDAP_LOOKUP_TASK_NAME: {
                "192.168.1.1": {"data": "some_data"},
                "10.0.0.5": {"data": "some_data"}
            }
        }
        expected_misses = []
        self.assertDictEqual(hits, expected_hits)
        self.assertEqual(misses, expected_misses)

    def test_find_all_cache_has_all_data_just_geo_ip(self):
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(EMPTY_CACHE))) as mo:
            self.in_memory_cache.update(FIND_ALL_TEST_CACHE)
        hits, misses = self.in_memory_cache.find_all(["10.0.0.5", "8.8.8.8"], just_geo=True)
        expected_hits = {
            GEO_IP_LOOKUP_TASK_NAME: {
                "8.8.8.8": {"data": "some_data"},
                "10.0.0.5": {"data": "some_data"}
            }
        }
        expected_misses = []
        self.assertDictEqual(hits, expected_hits)
        self.assertEqual(misses, expected_misses)

    def test_find_all_cache_has_partial_data_all_queries(self):
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(EMPTY_CACHE))) as mo:
            self.in_memory_cache.update(FIND_ALL_TEST_CACHE)
        hits, misses = self.in_memory_cache.find_all(["192.168.1.1"])
        expected_hits = {
            RDAP_LOOKUP_TASK_NAME: {},
            GEO_IP_LOOKUP_TASK_NAME: {}
        }
        expected_misses = ["192.168.1.1"]
        self.assertDictEqual(hits, expected_hits)
        self.assertEqual(misses, expected_misses)

    def test_find_all_cache_has_partial_data_just_rdap(self):
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(EMPTY_CACHE))) as mo:
            self.in_memory_cache.update(FIND_ALL_TEST_CACHE)
        hits, misses = self.in_memory_cache.find_all(["8.8.8.8"], just_rdap=True)
        expected_hits = {
            RDAP_LOOKUP_TASK_NAME: {}
        }
        expected_misses = ["8.8.8.8"]
        self.assertDictEqual(hits, expected_hits)
        self.assertEqual(misses, expected_misses)

    def test_find_all_cache_has_partial_data_just_geo(self):
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(EMPTY_CACHE))) as mo:
            self.in_memory_cache.update(FIND_ALL_TEST_CACHE)
        hits, misses = self.in_memory_cache.find_all(["192.168.1.1"], just_geo=True)
        expected_hits = {
            GEO_IP_LOOKUP_TASK_NAME: {}
        }
        expected_misses = ["192.168.1.1"]
        self.assertDictEqual(hits, expected_hits)
        self.assertEqual(misses, expected_misses)
