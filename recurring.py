import argparse
import sys
import logging

from internal.consolidator import Consolidator
from internal.core import config_stdout_logger
from internal.core_processing import create_recurring_report_from, process_command_line
from internal.entry_reporter import EntriesReporter

logger: logging.Logger


def process_commands_from_stdin_pipe():
    logger_level = logging.CRITICAL
    logging.basicConfig(level=logger_level)
    logger=config_stdout_logger(logging.getLogger(__name__), logger_level)

    reporter = EntriesReporter(logger=logger)
    consolidator = Consolidator(reporter)

    for line in sys.stdin.readlines():
        process_command_line(consolidator, reporter, line)
    
    logger.debug(consolidator.to_json())

    if consolidator.has_any_data():
        sys.stdout.writelines(create_recurring_report_from(consolidator))

def process_commands_from_loading_file():
    parser = argparse.ArgumentParser(
        prog='recurring',
        epilog="Thanks for using %(prog)s! :)",
        description="GFM recurring donations",
        add_help=True,
        allow_abbrev=True,
        )
    
    parser.add_argument('filename', type=str, nargs=1, help="Filename to process")
    parser.add_argument('-v', '--verbose', action="store_true")
    
    args = parser.parse_args()
    
    if not args.verbose:
        logger_level=logging.CRITICAL
    else:
        logger_level=logging.INFO

    logging.basicConfig(level=logger_level)

    logger=config_stdout_logger(logging.getLogger(__name__), logger_level)

    reporter = EntriesReporter(logger=logger)
    consolidator = Consolidator(reporter)

    filename = str(args.filename[0])
    try:
        source_file = open(filename, 'r', encoding='utf-8')
    except FileNotFoundError:
        logger.error(f"Unable to read file {filename}")
    else:
        with source_file:
            for line in source_file:
                process_command_line(consolidator, reporter, line)

    logger.debug(consolidator.to_json())

    if consolidator.has_any_data():
        sys.stdout.writelines(create_recurring_report_from(consolidator))


if __name__ == "__main__":

    if sys.stdin.readable() and not sys.stdin.isatty():
        process_commands_from_stdin_pipe()
    elif len(sys.argv) > 1:
        process_commands_from_loading_file()