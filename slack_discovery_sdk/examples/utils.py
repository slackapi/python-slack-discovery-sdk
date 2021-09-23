# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import platform, string, random, time, datetime, logging, os, re, pathlib, json, sys, time

from typing import Dict, Union, Optional, Any
from urllib.parse import urljoin

FILE_EXTENSION = '.json'

def export_json_to_file(new_items, logs_type):
    """This method is used to save data from the eDiscovery, DLP, and SIEM call patterns.
    This is just for example use, to make our partners and customers life easier. This is 
    not meant to be a production implementation by any means.
    Args:
        new_items: this is the JSON response from the discovery APIs that we want to save.
    Returns:
        None
    """

    todays_folder = create_folder()

    file_name = logs_type + FILE_EXTENSION

    with open(os.path.join(todays_folder, file_name), "a") as outfile:
        outfile.write(new_items)

    return None

def is_credit_card_number(credit_card) -> bool:
    valid_structure = r"[456]\d{3}(-?\d{4}){3}$"
    no_four_repeats = r"((\d)-?(?!(-?\2){3})){16}"
    filters = valid_structure, no_four_repeats

    if all(re.match(f, credit_card) for f in filters):
        return True
    else:
        return False

def get_current_timestamp() -> float:
    ts = time.time()
    return ts

def get_random_string(length: int = 10) -> str:
    all_ascii_lowercase_chars = string.ascii_lowercase
    random_string = "".join(random.choice(all_ascii_lowercase_chars) for _ in range(length))
    return random_string

def get_date_today() -> str:
    current_day = datetime.date.today()
    print("\n Default Date Object:", current_day, "\n")
 
    formatted_date = datetime.date.strftime(current_day, "%m_%d_%Y")
    print("\n Formatted Date String:", formatted_date, "\n")
    return formatted_date

def create_folder() -> str:
    """This method will create a folder to keep all output from the discovery calls 
    organized. It will create a folder based on MM-DD-YYYY United States date format. 
    Args:
        None
    Returns:
        None
    """

    current_day = datetime.date.today()

    formatted_date = datetime.date.strftime(current_day, "%m_%d_%Y")
    print("\n Formatted Date String:", formatted_date, "\n")

    todays_date_path = formatted_date + '_eDiscovery_output'
    print(todays_date_path)
    if not os.path.exists(todays_date_path):
        os.makedirs(todays_date_path)

    return todays_date_path


def get_timestamp_last_minute() -> int:
    now = time.time()
    seconds_in_one_minute = 60
    one_minute_ago = now - seconds_in_one_minute
    return int(one_minute_ago)

def create_draft() -> any:
    kwargs = None

    blocks = [{
		"block_id": "",
		"elements": [{
			"elements": [{
				"text": "testing the create draft API",
				"type": "text"
			}],
			"type": "rich_text_section"
		}],
		"type": "rich_text"
	}]

    kwargs.update(
            {
                "blocks": blocks,
                "client_msg_id": client_msg_id,
                "destinations": destinations,
                "file_ids": file_ids,
                "is_from_composer": is_from_composer,
            }
        )
    return self.api_call(
            "drafts.create", http_method="POST", params=kwargs
        )
