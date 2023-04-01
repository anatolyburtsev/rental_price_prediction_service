import logging
import argparse

from io_lib import store_json_to_csv, dummy_store_data
from zumper_lib import get_all_listings

logger = logging.getLogger()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", help="city to fetch data about", default="vancouver-bc")
    parser.add_argument("-o", "--output_prefix", help="output filename prefix. It will be suffixed with current time",
                        default="output")
    parser.add_argument("-f", "--output_format", help="output format", default="csv", choices=["csv", "dummy"])
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        raise Exception("To be implemented")

    all_data = get_all_listings(args.city)
    if args.output_format == "csv":
        store_json_to_csv(all_data, filename_prefix=f"{args.output_prefix}_{args.city}")
    else:
        dummy_store_data(all_data)

