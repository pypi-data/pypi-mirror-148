import unittest
from unittest import mock
from iplkp.lookup.rdap import rdap_lookup, fetch_rdap, RDAP_LOOKUP_ERROR_KEY

class TestRdap(unittest.IsolatedAsyncioTestCase):
    @mock.patch("aiohttp.ClientSession")
    async def test_fetch_rdap_status_200(self, mock_get):
        mocked_response_data = {"query": "8.8.8.8", "status": 200, "other_data": "data"}
        
        
        request_mock = mock.AsyncMock()
        request_mock.__aenter__.return_value = request_mock
        request_mock.json.return_value = mocked_response_data
        request_mock.status = 200

        mock_get.get.return_value = request_mock

        expected_response = {
            "8.8.8.8": {"query": "8.8.8.8", "status": 200, "other_data": "data"},
        }
        response = await fetch_rdap("http://mock-url.com", "8.8.8.8", mock_get)
        self.assertDictEqual(response, expected_response)

    
    async def test_rdap_lookup(self):
        with mock.patch("asyncio.gather", new=mock.AsyncMock()) as mock_gather:
            await rdap_lookup(["8.8.8.8"])
            mock_gather.assert_called_once()
    