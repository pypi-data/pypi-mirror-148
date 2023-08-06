"""
This module contains all features related to querying information
regarding RDAP data.
"""
import asyncio
from itertools import cycle
import aiohttp
from iplkp.utils import show_remaining_tasks
from iplkp.consts import (
    RDAP_CONNECTIONS_LIMIT,
    RDAP_CONNECTIONS_LIMIT_PER_HOST,
    RDAP_LOOKUP_TASK_PREFIX,
    IPLKP_EXCEPTION_KEY)

RDAP_LOOKUP_ERROR_KEY = "iplkp_rdap_error"

RDAP_URLS = {
    'arin': 'http://rdap.arin.net/registry/ip/',
    'ripencc': 'http://rdap.db.ripe.net/ip/',
    'apnic': 'http://rdap.apnic.net/ip/',
    'lacnic': 'http://rdap.lacnic.net/rdap/ip/',
    'afrinic': 'http://rdap.afrinic.net/rdap/ip/'
}

def parse_rdap_lookup_content(ip_address, status, content):
    """Transforms raw json data into rdap_lookup formatted output.

    Args:
      content:
        Raw HTTP response json data.

    Returns:
      A dict where keys are IP addresses and their values are dicts
      that contain RDAP information for each IP.
    """
    results = {}
    if status != 200:
        results[ip_address] = {
            RDAP_LOOKUP_ERROR_KEY: status,
            "message": "Error fetching RDAP info for the given IP"
        }
    else:
        results[ip_address] = content
    return results

async def fetch_rdap(url, ip_address, session):
    """Fetches RDAP data from RDAP_URLS.

    This asynchronous task sends a GET request that contains
    one IP address each, and parse the response before returning it.

    Args:
      url:
        URL from RDAP_URLS to send query to
      ip_address:
        IP addresses to include in the request
      session:
        Aiohttp session to send the request from

    Returns:
      Dicts containing information about the IP and it's RDAP data.
    """
    query_url = f"{url}{ip_address}"
    try:
        async with session.get(query_url) as response:
            show_remaining_tasks()
            content = await response.json()
            return parse_rdap_lookup_content(ip_address, response.status, content)
    except Exception as exception:
        return {
            ip_address: {
                IPLKP_EXCEPTION_KEY: f"Exception while calling fetch_rdap: {repr(exception)}"
            }
        }

async def rdap_lookup(ip_list):
    """Sets up asynchronous tasks for fetching RDAP information.

    Args:
      ip_list:
        List of ip addresses

    Returns:
      A dict mapping a RDAP key to dicts containing information about IPs
      and their RDAP data. Example:

      {"rdap_lookup":
        {"192.168.1.1":
          {"asn": ...}
        , "8.8.8.8": {
          {"asn": ...}
        }
      }
    """
    tasks = []
    rdap_urls = cycle(RDAP_URLS.values())
    timeout = aiohttp.ClientTimeout(total=None, sock_connect=10, sock_read=60)
    connector = aiohttp.TCPConnector(limit=RDAP_CONNECTIONS_LIMIT,
                                    limit_per_host=RDAP_CONNECTIONS_LIMIT_PER_HOST)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as rdap_session:
        for task_number, ip_address in enumerate(ip_list):
            url = next(rdap_urls)
            task = asyncio.create_task(
                fetch_rdap(url, ip_address, rdap_session), name=f"{RDAP_LOOKUP_TASK_PREFIX}{task_number}")
            tasks.append(task)
        task_results = await asyncio.gather(*tasks)
    responses = {}
    for result in task_results:
        responses |= result
    return responses
