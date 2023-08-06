"""The module provides a function of conversion from dictionary to JSON"""

import json
from logging import getLogger
from typing import List

logger = getLogger()


def to_json(content: List[tuple]) -> str:
    """Converts list containing news items into JSON string

    Args:
        content: List containing the news items

    Returns:
        JSON formatted string of serialized (converted) objects
    """
    logger.debug('Serializing to JSON...')
    json_list = []
    for item in content:
        json_item = {
            'Feed Title': item[1],
            'Feed Source': item[0],
            'News Item': {
                'News Title': item[2],
                'Publication Date': item[3],
                'Description': item[4],
                'Link': item[5],
                'Image Link': item[6]
            }
        }
        json_list.append(json_item)
    logger.debug('Serialization complete!')
    return json.dumps(json_list, indent=4)


def output_to_console(content: List[tuple]) -> None:
    """Outputs the contents of the parsed feed-containing XML

    Args:
        content: List containing the news items

    Returns:
        None
    """
    for item in content:
        print(f"\nFeed Title: {item[1]}\n")
        print(f"News Title: {item[2]}")
        print(f"Date Published: {item[3]}")
        print(f"Description: {item[4]}")
        print(f"Link: {item[5]}")
        print(f"Image: {item[6]}")
        print('\n====================================================================================\n')
