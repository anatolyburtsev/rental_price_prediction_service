import logging
import argparse

from io_lib import store_json_to_csv_local_file, dummy_store_data, store_json_to_csv_s3
from zumper_lib import get_all_listings

logger = logging.getLogger()

# TODO: replace choices with enums
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", help="city to fetch data about", default="vancouver-bc")
    parser.add_argument("-o", "--output_prefix", help="output filename prefix. It will be suffixed with current time",
                        default="output")
    parser.add_argument("-d", "--destination", help="where save file to", default="local", choices=["local", "s3"])
    parser.add_argument("-f", "--output_format", help="output format", default="csv", choices=["csv", "dummy"])
    parser.add_argument("-s3", "--s3_path", help="s3 path to save data to. Mandatory if destination is s3")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-fpo", "--first_page_only", help="download just first page of listings", default=False,
                        action="store_true")

    args = parser.parse_args()

    if args.verbose:
        raise Exception("To be implemented")

    all_data = get_all_listings(args.city, args.first_page_only)
    if args.output_format == "dummy":
        dummy_store_data(all_data)
    elif args.destination == "local":
        store_json_to_csv_local_file(all_data, filename_prefix=f"{args.output_prefix}_{args.city}")
    elif args.destination == "s3":
        if not args.s3_path:
            raise Exception("s3_path must be specified if destination is s3")
        store_json_to_csv_s3(all_data, args.s3_path, filename_prefix=f"{args.output_prefix}_{args.city}")
