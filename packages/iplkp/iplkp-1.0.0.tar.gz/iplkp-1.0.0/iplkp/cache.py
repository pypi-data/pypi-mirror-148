"""
The cache module contains all logic related to iplkp's
caching features.
"""
import json
from iplkp.consts import RDAP_LOOKUP_TASK_NAME, GEO_IP_LOOKUP_TASK_NAME, CACHE_DATASOURCE


class IplkpCacheException(Exception):
    """
    Raised when there's an error during initialization or
    use of the cache.
    """


class IplkpCache():
    """
    Contains utility methods for creating and updating an iplkp cache data source.
    """
    def __init__(self):
        self._data_source = self._init_from_file()

    def _init_empty(self):
        return {
            RDAP_LOOKUP_TASK_NAME: {},
            GEO_IP_LOOKUP_TASK_NAME: {}
        }

    def _init_from_file(self):
        try:
            with open(CACHE_DATASOURCE, "r", encoding="utf-8") as data_source:
                data = json.load(data_source)
                required_keys = [RDAP_LOOKUP_TASK_NAME, GEO_IP_LOOKUP_TASK_NAME]
                if not all(key in data for key in required_keys):
                    raise ValueError("Invalid cache file")
        except Exception as exception:
            print(f"Unable to read from cache data source ({exception})." + \
                "Starting with empty cache.")
        else:
            return data

        try:
            with open(CACHE_DATASOURCE, "w", encoding="utf-8") as data_source:
                file_structure = self._init_empty()
                json.dump(file_structure, data_source)
        except Exception as exception:
            raise IplkpCacheException(f"Unable to create cache file ({exception})")
        else:
            return file_structure

    def get_rdap(self, ip_address):
        """
        Indicates whether or not the given ip_address is cached within this instance
        rdap data
        """
        return ip_address in self._data_source[RDAP_LOOKUP_TASK_NAME]

    def get_geo_ip(self, ip_address):
        """
        Indicates whether or not the given ip_address is cached within this instance
        geo ip data
        """
        return ip_address in self._data_source[GEO_IP_LOOKUP_TASK_NAME]

    def update(self, results):
        """
        Updates the current cache instance with the given results
        """
        for key in results.keys():
            self._data_source[key] |= results[key]
        with open(CACHE_DATASOURCE, "w", encoding="utf-8") as new_data_source:
            json.dump(self._data_source, new_data_source)

    def find_all(self, addresses, just_rdap=False, just_geo=False):
        """Input:
            - a list of ip addresses
            - true or false if it's an rdap query
            - true or false if it's a geo_ip query
            (both true means it's both an rdap and geo_ip query)

            Returns:
            - two lists:
                - the first one with addresses found inside the cache
                - the seconds with addresses not in the cache

            an address is considered to be in the cache if
            - it's an rdap_query and the cache contains rdap info about the address
            - it's a geo_ip query and the cache contains geo_ip info about the address
            - it's both an rdap and geo_ip query, and the cache contains info
              about both for the given ip
        """
        cached_results = self._init_empty()
        missing_ips = []

        query_all = just_rdap == just_geo

        rdap_cached_results = cached_results[RDAP_LOOKUP_TASK_NAME]
        geo_ip_cached_results = cached_results[GEO_IP_LOOKUP_TASK_NAME]

        for ip in addresses:
            if query_all:
                if all([self.get_rdap(ip), self.get_geo_ip(ip)]):
                    rdap_cached_results[ip] = self._data_source[RDAP_LOOKUP_TASK_NAME][ip]
                    geo_ip_cached_results[ip] = self._data_source[GEO_IP_LOOKUP_TASK_NAME][ip]
                else:
                    missing_ips.append(ip)
            elif just_rdap:
                if self.get_rdap(ip):
                    rdap_cached_results[ip] = self._data_source[RDAP_LOOKUP_TASK_NAME][ip]
                else:
                    missing_ips.append(ip)
            elif just_geo:
                if self.get_geo_ip(ip):
                    geo_ip_cached_results[ip] = self._data_source[GEO_IP_LOOKUP_TASK_NAME][ip]
                else:
                    missing_ips.append(ip)

        # Remove the keys the user didn't ask for
        if not query_all and just_geo:
            del cached_results[RDAP_LOOKUP_TASK_NAME]
        if not query_all and just_rdap:
            del cached_results[GEO_IP_LOOKUP_TASK_NAME]

        print("returning cached results for " + \
            f"{min([len(cached_results[k]) for k in cached_results.keys()])} IPs" + \
            f", missing {len(missing_ips)}")
        return cached_results, missing_ips
