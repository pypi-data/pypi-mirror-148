import re
import sys
import json
import time
import aiohttp
import asyncio

from itertools import cycle

LIMIT = 5
LIMIT_PER_HOST = 1
RDAP_URL = "https://rdap-bootstrap.arin.net/bootstrap/ip/"
IP_URL = "http://ip-api.com/batch"
RDAP_LOOKUP_TASK_NAME = "rdap_lookup"
IP_LOOKUP_TASK_NAME = "ip_lookup"
RDAP_LOOKUP_TASK_PREFIX = f"{RDAP_LOOKUP_TASK_NAME}_task_"
IP_LOOKUP_TASK_PREFIX = f"{IP_LOOKUP_TASK_NAME}_task_"
MAX_IPs_PER_BATCH = 100
# API says max is 15 every 60 seconds, which translates to 1 every 4 seconds. Using 5 just to have some wiggle room.
SECONDS_BETWEEN_REQUESTS = 5
LOOKUP_ERROR_KEY = "iplkp_error"

RDAP_URLS = {
    'arin': 'http://rdap.arin.net/registry/ip/',
    'ripencc': 'http://rdap.db.ripe.net/ip/',
    'apnic': 'http://rdap.apnic.net/ip/',
    'lacnic': 'http://rdap.lacnic.net/rdap/ip/',
    'afrinic': 'http://rdap.afrinic.net/rdap/ip/'
}

def show_remaining_tasks():
    def is_lookup_task(task):
        is_ip_lookup = task.get_name().startswith(IP_LOOKUP_TASK_PREFIX)
        is_rdap_lookup = task.get_name().startswith(RDAP_LOOKUP_TASK_PREFIX)
        return any([is_ip_lookup, is_rdap_lookup])
    remaining_tasks = len([t for t in asyncio.all_tasks() if is_lookup_task(t)])
    print(f"Remaining queries: {remaining_tasks}    \r", end="", flush=True)

def get_ips():
    addr_args = []
    re_ip = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    try:
        with open("list_of_ips.txt", "r") as ip_file:
            lines = ip_file.readlines()
    except Exception as e:
        print(e)
        sys.exit(1)
    else:
        for line in lines:
            addr_args.extend(re.findall(re_ip, line))
    return addr_args

def parse_rdap_lookup_content(ip, status, content):
    results = {}
    if status != 200:
        results[ip] = {
            LOOKUP_ERROR_KEY: status,
            "message": "Error fetching RDAP info for the given IP"
        }
    else:
        results[ip] = content
    return results

async def fetch_rdap(url, ip, session):
    query_url = f"{url}{ip}"
    try:
        async with session.get(query_url) as response:
            #print(f"Remaining RDAP lookup requests: {len([t for t in asyncio.all_tasks() if t.get_name().startswith(RDAP_LOOKUP_TASK_PREFIX)])}")
            show_remaining_tasks()
            content = await response.json()
            return parse_rdap_lookup_content(ip, response.status, content)
    except Exception as e:
        print(repr(e))
        return {ip: {"iplkp_exception": repr(e)}}

async def rdap_lookup(ip_list):
    tasks = []
    rdap_urls = cycle(RDAP_URLS.values())
    timeout = aiohttp.ClientTimeout(total=None, sock_connect=10, sock_read=60)
    connector = aiohttp.TCPConnector(limit=LIMIT, limit_per_host=LIMIT_PER_HOST)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as rdap_session:
        for task_number, ip in enumerate(ip_list):
            url = next(rdap_urls)
            task = asyncio.create_task(fetch_rdap(url, ip, rdap_session), name=f"{RDAP_LOOKUP_TASK_PREFIX}{task_number}")
            tasks.append(task)
        task_results = await asyncio.gather(*tasks)
    responses = {}
    for t in task_results:
        responses |= t
    return responses

def parse_ip_lookup_content(content):
    results = {}
    for c in content:
        query = c["query"]
        status = c["status"]

        if status != "success":
            results[query] = {
                LOOKUP_ERROR_KEY: status,
                "message": c["message"]
            }
        else:
            results[query] = c
    return results

async def fetch_ip_batch(ip_bucket, delay, session):
    # hack to avoid having to deal with the API's rate limit dynamically.
    # We just schedule the requests at a rate that will never go over the limit
    await asyncio.sleep(delay)
    
    try:
        async with session.post(IP_URL, data=json.dumps(ip_bucket)) as response:
            #print(f"Remaining IP batch lookup requests: {len([t for t in asyncio.all_tasks() if t.get_name().startswith(IP_LOOKUP_TASK_PREFIX)])}")
            show_remaining_tasks()
            content = await response.json()
            return parse_ip_lookup_content(content)
    except Exception as e:
        return f"Exception while calling fetch_ip_batch: {repr(e)}"

async def ip_lookup(ip_list):
    tasks = []
    timeout = aiohttp.ClientTimeout(total=None, sock_connect=15, sock_read=15)
    connector = aiohttp.TCPConnector(limit=1, limit_per_host=1, force_close=True)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as ip_session:
        delay = 0
        for task_number, ip_bucket in enumerate(generate_buckets(ip_list, MAX_IPs_PER_BATCH)):
            task = asyncio.create_task(fetch_ip_batch(ip_bucket, delay, ip_session), name=f"{IP_LOOKUP_TASK_PREFIX}{task_number}")
            delay += SECONDS_BETWEEN_REQUESTS
            tasks.append(task)
        task_results = await asyncio.gather(*tasks)
    responses = {}
    for t in task_results:
        responses |= t
    return responses

def generate_buckets(lst, n):
    """Yield successive n-sized buckets from lst"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

async def run_queries(ip_list, just_rdap=False, just_ip=False):
    tasks = []
   
    query_all = not any([just_rdap, just_ip])

    if just_rdap or query_all:
        task_rdap = asyncio.create_task(rdap_lookup(ip_list), name=RDAP_LOOKUP_TASK_NAME)
        tasks.append(task_rdap)

    if just_ip or query_all:
        task_ip = asyncio.create_task(ip_lookup(ip_list), name=IP_LOOKUP_TASK_NAME)
        tasks.append(task_ip)

    if tasks:
        await asyncio.gather(*tasks)
        return {task.get_name():task.result() for task in tasks}
    else:
        return {}

def main(ip_list, just_rdap=False, just_ip=False):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    time_start = time.time()
    r = asyncio.run(run_queries(ip_list, just_rdap=just_rdap, just_ip=just_ip))
    time_end = time.time()
    print(f"Operation took {round(time_end - time_start, 1)} seconds")
    return r

def testing(ip_number, just_rdap=False, just_ip=False):
    ips = get_ips()
    print(f"got {len(ips)} ips\n")
    return main(ips[:ip_number], just_rdap=just_rdap, just_ip=just_ip)






























async def fetch_ip(url, session, rate_limit_reached):
    try:
        # We need to remove the while == True, and use a semaphore and update it outside this async with call,
        # otherwise, a million requests could be crafted and sent, and will reach the API even
        # before hitting the rate_limit_reached event.
        async with session.get(url) as response:
            content = await response.json()
            if content["status"] == "fail":
                hernan_content = content["message"]
            elif content["status"] == "success":
                hernan_content = content["country"]
            else:
                hernan_content = "API undocumented error"
            pending_requests = len([t for t in asyncio.all_tasks() if t.get_name().startswith('ip_lookup_task')])
            print(f"Remaining IP lookup requests: {pending_requests}")
            try:
                remaining_limit = int(response.headers["X-Rl"])
                sec = int(response.headers["X-Ttl"])
                print(f"limit: {remaining_limit} requests, reset in: {sec} seconds")
            except Exception as e:
                for t in asyncio.all_tasks():
                    if t.get_name().startswith(IP_LOOKUP_TASK_PREFIX):
                        t.cancel("Task cancelled because we can't parse remaining limit")
                raise ValueError("Couldn't fetch remaining limit to query API. Will consider remaining limit as 0. This is an unrecoverable error")
            else:
                if remaining_limit <= 0:
                    print(f"coroutine hit rate_limit, now we'll wait for {sec} seconds")
                    rate_limit_reached.set()
                    await asyncio.sleep(sec + 1)
                    rate_limit_reached.clear()
            return (url, response.status, {"hernan_content": hernan_content, "remaining-limit": remaining_limit, "seconds-until-reset": sec})
    except Exception as e:
        print(repr(e))
        return (url, "ERROR", str(e))