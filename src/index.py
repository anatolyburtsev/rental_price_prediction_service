import os
from datetime import datetime

from io_lib import store_json_to_csv_s3
from zumper_lib import get_all_listings, get_xz_token
import logging

logger = logging.getLogger()


def process_city(city, s3_bucket, today):
    logging.info(f"Start processing {city}")
    xz_token = get_xz_token()
    logger.info(f"XZ token: {xz_token}")
    data = get_all_listings(city, xz_token=xz_token)
    if not data:
        logging.error(f"No data for {city}")
        return
    store_json_to_csv_s3(data, f's3://{s3_bucket}/zumper_data/{city}', filename_prefix=f"dump_{city}", today=today)
    logging.info(f"finished processing {city}")


def fetch_zumper_data_handler(event, lambda_context):
    with open("zumper_city_urls.txt", "r") as f:
        cities = f.readlines()
    s3_bucket = os.environ.get("S3_BUCKET_NAME")
    today = datetime.now()

    for city in cities:
        process_city(city.replace("\n", ""), s3_bucket, today)

    return {"status": "Success"}
