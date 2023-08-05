"""The module provides a function of conversion from dictionary to JSON"""

import json
import logging
from typing import Union, List

logger = logging.getLogger()


def to_json(parsed_content: List[Union[str, dict]]) -> str:
    """Converts list containing dictionary elements to JSON

    Args:
        parsed_content: List containing the parsed feed source and the parsed news items

    Returns:
        JSON formatted string of serialized (converted) objects
    """
    logger.debug('Serializing to JSON...')
    json_list = []
    for item in parsed_content[1:]:
        json_item = {
            'Feed Source': parsed_content[0],
            'News Item': {
                'Title': item['title'],
                'Publication Date': item['pub_date'],
                'Description': item['description'],
                'Link': item['link']
            }
        }
        json_list.append(json_item)
    logger.debug('Serialization complete!')
    return json.dumps(json_list, indent=4)
