import unittest
from unittest import mock
from iplkp.lookup.geo_ip import geo_ip_lookup, fetch_ip_batch, GEO_IP_LOOKUP_ERROR_KEY

class TestGeoIp(unittest.IsolatedAsyncioTestCase):
    @mock.patch("aiohttp.ClientSession")
    async def test_fetch_ip_batch(self, mock_post):
        mocked_response_data = [
            {"query": "8.8.8.8", "status": "success", "other_data": "data"},
            {"query": "192.168.1.1", "status": "not_success", "message": "description of error"},
        ]
        
        request_mock = mock.AsyncMock()
        request_mock.__aenter__.return_value = request_mock
        request_mock.json.return_value = mocked_response_data

        mock_post.post.return_value = request_mock

        expected_response = {
            "8.8.8.8": {"query": "8.8.8.8", "status": "success", "other_data": "data"},
            "192.168.1.1": {GEO_IP_LOOKUP_ERROR_KEY: "not_success", "message": "description of error"}
        }
        response = await fetch_ip_batch(["8.8.8.8"], 0, mock_post)
        self.assertDictEqual(response, expected_response)

    async def test_geo_ip_lookup(self):
        with mock.patch("asyncio.gather", new=mock.AsyncMock()) as mock_gather:
            await geo_ip_lookup(["8.8.8.8"])
            mock_gather.assert_called_once()
