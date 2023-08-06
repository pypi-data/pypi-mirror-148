"""
This module contains constants relevant across the application
"""

IPLKP_DESC = "iplkp - Geo IP and RDAP lookup tool"
GEO_IP_LOOKUP_TASK_NAME = "ip_lookup"
GEO_IP_LOOKUP_TASK_PREFIX = f"{GEO_IP_LOOKUP_TASK_NAME}_task_"
RDAP_LOOKUP_TASK_NAME = "rdap_lookup"
RDAP_LOOKUP_TASK_PREFIX = f"{RDAP_LOOKUP_TASK_NAME}_task_"
IPLKP_EXCEPTION_KEY = "iplkp_exception"
RDAP_CONNECTIONS_LIMIT = 5
RDAP_CONNECTIONS_LIMIT_PER_HOST = 1
CACHE_DATASOURCE = "cache.json"
