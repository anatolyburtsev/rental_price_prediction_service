import requests
from constants import XZ_TOKEN_URL, LISTING_URL, DEFAULT_LISTING_REQUEST_PARAMS
import json
import logging


class ZumperAPIException(Exception):
    pass


def get_xz_token():
    resp = requests.get(XZ_TOKEN_URL)
    if not resp.ok:
        raise ZumperAPIException(f"Failed to get xz token. code: {resp.status_code}, response: {resp.text}")
    return json.loads(resp.text)["xz_token"]


def _get_xz_headers(xz_token):
    # xz_tokens = get_xz_tokens() if xz_token is None else xz_token
    return {
        "X-Zumper-XZ-Token": xz_token,
    }


def _safe_get_key(object_, key):
    if key not in object_:
        logging.error(f"key: {key} not found in object: {object_}")
    return object_[key]


def _safe_parse_json(json_str):
    try:
        return json.loads(json_str)
    except Exception as e:
        logging.error(f"Failed to parse json: {json_str}")
        raise e


# url of city on zumper website
def get_all_listings(url, xz_token=None, one_page_only=False):
    headers = _get_xz_headers(xz_token=xz_token)
    listing_params = {
        **DEFAULT_LISTING_REQUEST_PARAMS,
        "url": url
    }
    raw_data = requests.post(LISTING_URL, headers=headers, json=listing_params)
    parsed_data = _safe_parse_json(raw_data.text)
    data = _safe_get_key(parsed_data, "listables")
    expected_total = _safe_get_key(parsed_data, "matching")
    logging.debug(f"Fetch first batch of data. Expected {expected_total} records")
    exclude_group_ids = []
    while len(exclude_group_ids) <= expected_total and not one_page_only:
        exclude_group_ids = [x["group_id"] for x in data]
        batch_raw = requests.post(LISTING_URL, headers=headers, json={
            **listing_params,
            "excludeGroupIds": str(exclude_group_ids)
        })

        batch = _safe_parse_json(batch_raw.text)["listables"]
        logging.debug(f"got {len(batch)} records")
        if len(batch) == 0:
            break
        data += batch
    return data
