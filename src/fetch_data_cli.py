import logging
import click

from io_lib import store_json_to_csv_local_file, dummy_store_data, store_json_to_csv_s3
from zumper_lib import get_all_listings

logger = logging.getLogger()


@click.command()
@click.option("--city", help="city to fetch data about (default: vancouver-bc)", default="vancouver-bc")
@click.option("-o", "--output_prefix",
              help="output filename prefix. It will be suffixed with current time (default: output)",
              default="output")
@click.option("-d", "--destination", help="where save file to (default: local)", default="local",
              type=click.Choice(["local", "s3"]))
@click.option("-f", "--output_format", help="output format (default: csv)", default="csv",
              type=click.Choice(["csv", "dummy"]))
@click.option("-s3", "--s3_path", help="s3 path to save data to. Mandatory if destination is s3")
@click.option("-v", "--verbose", help="increase output verbosity", is_flag=True)
@click.option("-fpo", "--first_page_only", help="download just first page of listings (default: False)", default=False,
              is_flag=True)
def main(city, output_prefix, destination, output_format, s3_path, verbose, first_page_only):
    if verbose:
        raise Exception("To be implemented")

    all_data = get_all_listings(city, first_page_only)
    if output_format == "dummy":
        dummy_store_data(all_data)
    elif destination == "local":
        store_json_to_csv_local_file(all_data, filename_prefix=f"{output_prefix}_{city}")
    elif destination == "s3":
        if not s3_path:
            raise Exception("s3_path must be specified if destination is s3")
        store_json_to_csv_s3(all_data, s3_path, filename_prefix=f"{output_prefix}_{city}")


if __name__ == '__main__':
    main()
