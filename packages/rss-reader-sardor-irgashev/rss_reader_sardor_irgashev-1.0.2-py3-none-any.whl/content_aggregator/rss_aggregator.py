"""The module provides implementation to aggregate RSS content"""

import logging
import sys
from typing import Union, List, Optional

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()


class RSSContent:
    """Represents RSS content aggregation"""

    def __init__(self, url: str, content_limit: Optional[int] = None) -> None:
        """Class constructor

        Args:
            url: Limit of the feeds
            content_limit: URL of RSS feed

        Returns:
            None
        """
        self.url = url
        self._content_limit = content_limit
        self._parsed_rss_content = []
        self._response_object = None

    def _fetch_rss_content(self) -> None:
        """Fetches RSS page based on URL

        Returns:
            None
        """
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        logger.debug(f'Making HTTP request to {self.url}')
        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            logger.error('Connection Error Occurred. Program Terminated. Try Again.')
            sys.exit()
        except requests.exceptions.HTTPError:
            logger.error('HTTP Error Occurred. Program Terminated. Try Again.')
            sys.exit()
        except requests.exceptions.URLRequired:
            logger.error('A valid URL is required to make a request. Program Terminated. Try Again.')
            sys.exit()
        except requests.exceptions.TooManyRedirects:
            logger.error('Too many redirects. Program Terminated. Try Again.')
            sys.exit()
        except requests.exceptions.Timeout:
            logger.error('The Request Timed Out. Program Terminated. Try Again.')
            sys.exit()
        except requests.exceptions.RequestException:
            logger.error('Ambiguous Exception. Program Terminated. Try Again.')
            sys.exit()
        self._response_object = response
        logger.debug('Response arrived!')

    def _parse_rss_content(self) -> None:
        """Parses the XML contents of the Response object

        Returns:
            None
        """
        logger.debug('Parsing fetched content...')
        soup = BeautifulSoup(self._response_object.text, 'xml')
        feed = soup.channel.title.text
        articles = soup.find_all('item', limit=self._content_limit)
        self._parsed_rss_content = [feed]
        for article in articles:
            news_item = {
                'title': article.title.text,
                'pub_date': article.pubDate.text if article.pubDate else 'No Publication Date',
                'description': article.description.text if article.description else 'No Description',
                'link': article.link.text,
            }
            self._parsed_rss_content.append(news_item)
        logger.debug('Parsing complete!')

    def get_parsed_rss_content(self) -> List[Union[str, dict]]:
        """Returns parsed RSS content

        Returns:
            List containing the parsed feed source and the parsed news items
        """
        self._fetch_rss_content()
        self._parse_rss_content()
        return self._parsed_rss_content


def output_to_console(parsed_content: List[Union[str, dict]]) -> None:
    """Prints the contents of the parsed feed-containing XML

    Args:
        parsed_content: List containing the parsed feed source and the parsed news items

    Returns:
        None
    """
    print(f"\nFeed: {parsed_content[0]}\n")
    for item in parsed_content[1:]:
        print(f"Title: {item['title']}")
        print(f"Date Published: {item['pub_date']}")
        print(f"Description: {item['description']}")
        print(f"Link: {item['link']}")
        print('\n====================================================================================\n')
