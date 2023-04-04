import json
import logging
from datetime import datetime
import pandas as pd
import awswrangler as wr
import os


def _json_to_df(data):
    data_json = json.dumps(data)
    df = pd.read_json(data_json)
    return df


def _get_filename(prefix: str, date: datetime):
    return f"{prefix}_{date.strftime('%Y-%m-%d-%H-%M')}.csv"


def store_json_to_csv_local_file(data, filename_prefix="output", today=datetime.now()):
    df = _json_to_df(data)
    logging.debug(f"dataframe size is {df.shape}")
    filename = _get_filename(filename_prefix, today)
    df.to_csv(filename, index=False)


def store_json_to_csv_s3(data, s3_path, filename_prefix="output", today=datetime.now()):
    df = _json_to_df(data)
    wr.s3.to_csv(
        df=df,
        path=os.path.join(s3_path, _get_filename(filename_prefix, today))
    )


def dummy_store_data(data):
    logging.info(f"data size is {len(data)}. Example of one line: {data[0]}")
