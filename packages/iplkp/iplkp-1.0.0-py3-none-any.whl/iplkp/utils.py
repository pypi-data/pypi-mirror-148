"""
iplkp utils module, which contains utility and helper
functions used across the application
"""

import argparse
import asyncio
import ipaddress
import os
import re
from iplkp.consts import GEO_IP_LOOKUP_TASK_PREFIX, RDAP_LOOKUP_TASK_PREFIX, IPLKP_DESC


class IplkpArgumentException(Exception):
    """
    Rased when there's an error while parsing input arguments
    """


def show_remaining_tasks():
    """
    Utility function that scans the list of tasks within the current event loop
    and shows a counter of RDAP and Geo IP tasks pending.
    """
    def is_lookup_task(task):
        is_ip_lookup = task.get_name().startswith(GEO_IP_LOOKUP_TASK_PREFIX)
        is_rdap_lookup = task.get_name().startswith(RDAP_LOOKUP_TASK_PREFIX)
        return any([is_ip_lookup, is_rdap_lookup])
    remaining_tasks = len([t for t in asyncio.all_tasks() if is_lookup_task(t)])
    print(f"Remaining queries: {remaining_tasks}     \r", end="", flush=True)


def parse_args(supplied_args):
    """
    Function that contains the input arguments parsing logic
    """
    parser = argparse.ArgumentParser(description=IPLKP_DESC)
    main_group = parser.add_mutually_exclusive_group(required=True)
    main_group.add_argument("-i",
                            "--ip-address",
                            dest="ip_addr",
                            metavar="IP_ADDR",
                            help="Fetch information for a single given IP address")
    main_group.add_argument("-b",
                            "--bulk",
                            dest="filename",
                            metavar="INPUT_FILE",
                            help="Read IP addresses in bulk from INPUT_FILE")

    query_group = parser.add_argument_group(title="Available queries")
    query_group.add_argument("-g",
                            "--geo-ip",
                            dest="just_geo",
                            help="Only query Geo IP information for the given " + \
                                "address or list of addresses",
                            action="store_true")
    query_group.add_argument("-r",
                            "--rdap",
                            dest="just_rdap",
                            help="Only query RDAP information for the given " + \
                                "address or list of addresses",
                            action="store_true")

    parser.add_argument("-o",
                        "--output",
                        dest="save_output",
                        metavar="OUTPUT_FILE",
                        help="Write output to a given OUTPUT_FILE")
    parser.add_argument("-f",
                        "--force",
                        dest="overwrite",
                        help="Overwrite contents of OUTPUT_FILE if it exists",
                        action="store_true")
    parser.add_argument("-c",
                        "--no-cache",
                        dest="use_cache",
                        help="Do not use cache to fetch results. Do not update " + \
                            "it after getting IP information",
                        default=True,
                        action="store_false")

    if len(supplied_args) == 1:
        parser.print_help()
        raise IplkpArgumentException("No arguments supplied")

    args = parser.parse_args()
    output_file_exists = args.save_output and os.path.isfile(args.save_output)
    if output_file_exists and not args.overwrite:
        raise IplkpArgumentException("Output file already exists. If you want to " + \
            "overwrite, you must pass the -f, --force flag.")

    return args


def parse_address_args(args):
    """
    Function that contains the business rules related to IP address parsing
    """
    addr_args = []
    valid_addrs = []
    invalid_addrs = []

    if args.ip_addr:
        addr_args.append(args.ip_addr)
    elif args.filename:
        re_ip = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        try:
            with open(args.filename, "r", encoding="utf-8") as ip_file:
                lines = ip_file.readlines()
        except (FileNotFoundError, OSError) as err:
            print(f"Couldn't read file {args.filename}: {str(err)}")
            return valid_addrs, invalid_addrs
        else:
            for line in lines:
                addr_args.extend(re.findall(re_ip, line))
    else:
        return valid_addrs, invalid_addrs

    for addr in addr_args:
        try:
            valid_addrs.append(str(ipaddress.ip_address(addr)))
        except ValueError:
            invalid_addrs.append(addr)
            continue

    if invalid_addrs:
        print(f"Found {len(invalid_addrs)} invalid IP addresses on " +\
            f"input: {invalid_addrs}")

    if valid_addrs:
        print(f"Found {len(valid_addrs)} valid IP addresses on " + \
            f"input: {valid_addrs}")
    else:
        print("No valid addresses found on input")

    return valid_addrs
