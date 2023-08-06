"""The module is the entry point for the RSS reader project"""

from logging import getLogger, config

from argument_parser.arg_parser import handle_args
from config import logging_config
from content_aggregator.rss_aggregator import RSSContent
from output_manager.console_output import to_json, output_to_console

config.dictConfig(logging_config)
logger = getLogger()
logger.disabled = True


def main() -> None:
    """The entry point function

    Returns:
        None
    """
    parser = handle_args()
    if parser.verbose:
        logger.disabled = False

    logger.debug('Program started.')
    rss_content = RSSContent(parser.source, parser.date, parser.limit)
    retrieved_rss_content = rss_content.retrieve_from_storage()
    logger.debug('Content retrieved.')

    if parser.json:
        print(to_json(retrieved_rss_content))
    else:
        output_to_console(retrieved_rss_content)


if __name__ == '__main__':
    main()
