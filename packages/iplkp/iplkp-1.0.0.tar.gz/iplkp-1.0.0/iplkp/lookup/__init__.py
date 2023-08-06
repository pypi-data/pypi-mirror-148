"""
The lookup module contains the logic related to IP lookup operations
"""
import asyncio
import time
from iplkp.lookup.geo_ip import geo_ip_lookup
from iplkp.lookup.rdap import rdap_lookup
from iplkp.consts import GEO_IP_LOOKUP_TASK_NAME, RDAP_LOOKUP_TASK_NAME
from iplkp.cache import IplkpCache, IplkpCacheException


async def run_queries(ip_list, just_rdap=False, just_geo=False):
    """Create asyncronous queries for RDAP and Geo IP lookups.

    Each query is wrapped into an asyncronous task and executed within an
    asyncio event loop, saving a lot of time in I/O wait.

    Args:
      ip_list:
        A list of IP addresses.
      just_rdap:
        True if only RDAP information should be queried. (default=False)
      just_geo:
        True if only Geo IP information should be queried. (default=False)

    Returns:
      A dict mapping an rdap key to dicts containing information about IPs and their
      rdap data, and a geo ip key mapping to dicts containing information about IPs
      and their geo ip data. Example:

      {"rdap_lookup":
        {"192.168.1.1":
          {"asn": ...}
        , "8.8.8.8": {
          {"asn": ...}
        },
       "ip_lookup":
        {"192.168.1.1":
          {"country": ...}
        , "8.8.8.8": {
          {"country": ...}
        }
      }
    """
    tasks = []

    query_all = not any([just_rdap, just_geo])

    if just_rdap or query_all:
        task_rdap = asyncio.create_task(rdap_lookup(ip_list), name=RDAP_LOOKUP_TASK_NAME)
        tasks.append(task_rdap)

    if just_geo or query_all:
        task_ip = asyncio.create_task(geo_ip_lookup(ip_list), name=GEO_IP_LOOKUP_TASK_NAME)
        tasks.append(task_ip)

    if tasks:
        await asyncio.gather(*tasks)
        return {task.get_name():task.result() for task in tasks}
    return {}


def lookup(ip_list, just_rdap=False, just_geo=False, use_cache=True):
    """Queries RDAP and/or Geo IP information about addresses.

    It also checks whether the information about any given IP is inside
    the application cache and can return that information, avoiding sending
    a request to an external server.

    Args:
      ip_list:
        A list of IP addresses.
      just_rdap:
        True if only RDAP information should be queried. (default=False)
      just_geo:
        True if only Geo IP information should be queried. (default=False)
      use_cache:
        True if results should be fetched from cache if possible. (default=True)

    Returns:
      A dict mapping an rdap key to dicts containing information about IPs and their
      rdap data, and a geo ip key mapping to dicts containing information about IPs
      and their geo ip data. Example:

      {"rdap_lookup":
        {"192.168.1.1":
          {"asn": ...}
        , "8.8.8.8": {
          {"asn": ...}
        },
       "ip_lookup":
        {"192.168.1.1":
          {"country": ...}
        , "8.8.8.8": {
          {"country": ...}
        }
      }
    """
    results = {}
    cache = None

    if use_cache:
        try:
            cache = IplkpCache()
        except IplkpCacheException as ex:
            print(f"{ex}. This is not an issue with iplkp. If the problem persists, " + \
                "try calling iplkp with --no-cache")
        else:
            cached_data, missing_ips = cache.find_all(ip_list,
                                                        just_rdap=just_rdap,
                                                        just_geo=just_geo)
            if not missing_ips:
                return cached_data
            ip_list = missing_ips

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    time_start = time.time()
    results = asyncio.run(run_queries(ip_list, just_rdap=just_rdap, just_geo=just_geo))
    time_end = time.time()

    if cache and use_cache:
        cache.update(results)
        for key in results.keys():
            results[key] |= cached_data[key]

    print(f"Operation took {round(time_end - time_start, 1)} seconds")

    return results
