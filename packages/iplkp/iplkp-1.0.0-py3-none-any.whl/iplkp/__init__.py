"""
iplkp main module. iplkp is a command line application which
helps looking up one or multiple IPs RDAP or Geo IP information.
"""

import json
import sys
from iplkp.lookup import lookup
from iplkp import utils

def main():
    """
    iplkp entry point. Parse arguments, lookup addresses
    and return or write results to file.
    """
    try:
        args = utils.parse_args(sys.argv)
    except utils.IplkpArgumentException as iplkp_arg_exception:
        print(f"{iplkp_arg_exception}")
        sys.exit(1)
    else:
        valid_addrs = utils.parse_address_args(args)

    if not valid_addrs:
        sys.exit(1)

    results = lookup(valid_addrs,
                    just_rdap=args.just_rdap,
                    just_geo=args.just_geo,
                    use_cache=args.use_cache)

    if args.save_output:
        with open(args.save_output, "w", encoding="utf-8") as output:
            json.dump(results, output)
    else:
        print(results)
    sys.exit(0)
