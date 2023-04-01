import json
import logging
from datetime import datetime
import pandas as pd


def store_json_to_csv(data, filename_prefix="output", today=datetime.now()):
    data_json = json.dumps(data)
    df = pd.read_json(data_json)
    logging.debug(f"dataframe size is {df.shape}")
    filename = f"{filename_prefix}_{today.strftime('%Y-%m-%d-%H-%M')}.csv"
    df.to_csv(filename, index=False)


def dummy_store_data(data):
    logging.info(f"data size is {len(data)}. Example of one line: {data[0]}")
