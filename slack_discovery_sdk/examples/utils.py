# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import datetime, os, re, shutil

FILE_EXTENSION = ".json"

## This file contains functions which will help create a directory structure to organize and
## hold the output from the discovery APIs. This is just meant as a helper to get you started,
## and is by no means a production ready solution. Use this to get familiar with the discovery APIs.


def export_json_to_file(new_items: str, logs_type: str, channel_id: str, user_id: str):
    """This method is used to save data from the eDiscovery, DLP, and SIEM call patterns.
    This is just for example use, to make our partners and customers life easier. This is
    not meant to be a production implementation by any means.
    Args:
        new_items: this is the JSON response from the discovery APIs that we want to save.
        logs_type: this is the discovery API method used
        channel_id: channel_id i.e C02449123
        user_id: The ID of the user i.e. U09123411
    Returns:
        None
    """
    if channel_id != None:
        channel_folder = create_folder_for_channel(channel_id, user_id)

    file_name = logs_type + FILE_EXTENSION

    with open(os.path.join(channel_folder, file_name), "a") as outfile:
        outfile.write(new_items)


def create_folder_for_channel(channel_id: str, user_id: str) -> str:
    """This method will create a folder to keep all output from the discovery calls
    organized. It will create a folder based on channelID for a particular user: for example C02642201.
    Args:
        None
    Returns:
        Str which resresents the channel
    """

    current_day = datetime.date.today()

    formatted_date = datetime.date.strftime(current_day, "%Y/%m/%d")

    path = formatted_date + "/" + user_id + "/" + channel_id + "/"

    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)  # Removes all the subdirectories!
        os.makedirs(path)

    return formatted_date + "/" + user_id + "/" + channel_id + "/"


def is_credit_card_number(credit_card: str) -> bool:
    valid_structure = r"[456]\d{3}(-?\d{4}){3}$"
    no_four_repeats = r"((\d)-?(?!(-?\2){3})){16}"
    filters = valid_structure, no_four_repeats

    if all(re.match(f, credit_card) for f in filters):
        return True
    else:
        return False
