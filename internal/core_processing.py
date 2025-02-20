
from functools import reduce
import sys
import traceback
from venv import logger

from internal.commands import Command
from internal.consolidator import Consolidator
from internal.entry_reporter import EntriesReporter


def extract_command(line: str) -> Command | None:
    """This functions takes a string and searches for Command subclasses that could handle and create an instance of themselves processing this string. If none is found it returns None.

        Keyword arguments:
        - line -- string that has to be evaluated by command classes.

        Returns:
        Command | None
    """
    for command_subclass in Command.__subclasses__():
        instance: Command | None = command_subclass.instantiate_from_string(line)
        if instance and instance.validate():
            return instance
        
    return None

def process_command_line(consolidator: Consolidator, reporter:EntriesReporter, line: str):
    """This functions takes a string and searches for Command subclasses that could handle and create an instance of themselves processing this string. If none is found it returns None.
    
        Keyword arguments:
        - consolidator -- Consolidator that will hold model data
        - reporter -- EntriesReporter that coordinates the generation of processing logs
    """
    logger.info(f"Processing line: {line}")
    try:
        command = extract_command(line)
        if command:
            logger.warning(f"Processing command: {command.__class__.__name__}")
            command.dispatch_to_executor(consolidator)
        else:
            reporter.report_skipped_input(line, f"Record got discarded, no command could be created for it: {line}")
    except Exception as e:
        _exc_type, _exc_value, exc_traceback = sys.exc_info()

        traces = traceback.extract_tb(exc_traceback)

        logger.debug(''.join(traces.format()))

        reporter.report_error_input(line, str(e))


def create_recurring_report_from(consolidator: Consolidator) -> str:
    """This creates a final report as text having the base of the consolidator with the following format:

            Donors:
            Greg: Total: $300 Average: $150
            ...
            Janine: Total: $50 Average: $50

            Campaigns:
            HelpTheKids: Total: $200
            ...
            SaveTheDogs: Total: $150
    
        Keyword arguments:
        - consolidator -- Consolidator that will hold model data
        Returns:
        str
    """

    if not consolidator:
        return ""
    
    results = []

    if len(consolidator.all_donors):
        results.append('Donors:')

        for donor in sorted(consolidator.all_donors, key=lambda donor: donor.name):
            average_expent = 0
            donated = 0

            if len(donor.donations):
                donated = reduce(lambda acumulator, donation : donation.get_donation_amount() + acumulator, donor.donations, 0)
                average_expent =  donated / len(donor.donations)
            
            results.append(f"{donor.name}: Total: ${donated} Average: ${average_expent}")
    
    if len(results) and len(consolidator.all_campaigns):
        results.append("")

    if len(consolidator.all_campaigns):
        results.append("Campaigns:")

        for campaign in sorted(consolidator.all_campaigns, key=lambda campaign: campaign.name):
            results.append(f"{campaign.name}: Total: ${campaign.funds}")


    return "\n".join(results)