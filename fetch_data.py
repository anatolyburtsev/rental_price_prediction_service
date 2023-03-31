import requests
import json
import logging
from datetime import datetime
import pandas as pd

from constants import XZ_TOKEN_URL, LISTING_URL, DEFAULT_LISTING_REQUEST_PARAMS

logger = logging.getLogger()


class ZumperAPIException(Exception):
    pass


def _get_xz_tokens():
    resp = requests.get(XZ_TOKEN_URL)
    if not resp.ok:
        logger.error(f"code: {resp.status_code}, response: {resp.text}")
        raise ZumperAPIException("Failed to get xz token")
    return json.loads(resp.text)


def _get_xz_headers():
    xz_tokens = _get_xz_tokens()
    return {
        "X-Zumper-XZ-Token": xz_tokens["xz_token"],
    }


def get_all_listings(listing_params):
    headers = _get_xz_headers()
    raw_data = requests.post(LISTING_URL, headers=headers, json=listing_params)
    parsed_data = json.loads(raw_data.text)
    data = parsed_data["listables"]
    expected_total = parsed_data["matching"]
    logging.debug(f"Fetch first batch of data. Expected {expected_total} records")
    exclude_group_ids = []
    while len(exclude_group_ids) <= expected_total:
        exclude_group_ids = [x["group_id"] for x in data]
        batch_raw = requests.post(LISTING_URL, headers=headers, json={
            **listing_params,
            "excludeGroupIds": str(exclude_group_ids)
        })

        batch = json.loads(batch_raw.text)["listables"]
        logging.debug(f"got {len(batch)} records")
        if len(batch) == 0:
            break
        data += batch
    return data


def store_json_to_csv(data, today=datetime.now()):
    data_json = json.dumps(data)
    df = pd.read_json(data_json)
    logging.debug(f"dataframe size is {df.shape}")
    filename = f"output_{today.strftime('%Y-%m-%d-%H-%M')}.csv"
    df.to_csv(filename, index=False)


if __name__ == '__main__':
    all_data = get_all_listings(DEFAULT_LISTING_REQUEST_PARAMS)
    store_json_to_csv(all_data)

