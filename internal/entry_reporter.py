
from datetime import datetime, timezone
from enum import Enum
import logging
from typing import Dict

from internal.commands import AddCampaign, AddDonation, AddDonor, Command
from internal.core import T, TIMESTAMP_FORMAT

class ReporterEntryStatus(str, Enum):
    """Enum that represents the different status a ReporterEntry can be in a given time"""
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"

class ReporterEntry(object):
    """ReporterEntry represents the result of processing a `target` that has the following attributes:

      - result_type: a status
      - description: str explaining the status, that's optional
      - target: the object onto this entry has been created
      - timestamp: a timestamp in UTC for the creation time of this entry"""
    
    def __init__(self, result_type: ReporterEntryStatus, description: str, target: T):
        """
            Constructor for this class

            Keyword arguments:

            - result_type -- status of this entry
            - description -- optional description that can be attached to this entry
            - target -- target object for which this entry has been created
        """
        self.result_type: ReporterEntryStatus = result_type
        self.description: str = description
        self.target:T = target
        self.timestamp: datetime = datetime.now(timezone.utc)

    def to_json_obj(self):
        """ Returns a string with a JSON representation of this object and it's relevant information"""
        return {key: (value.to_json_obj() 
                      if isinstance(value, Command) else (
                          value.strftime(TIMESTAMP_FORMAT) if isinstance(value, datetime) else value))
                    for key, value in self.__dict__.items()
                }

class EntriesReporter(object):
    """EntriesReporter creates and stores reporter entries for:
     
      - donors
      - campaigns
      - donations
      - input"""
    def __init__(self, logger:logging.Logger):
        """Constructor for this class
        
        Keyword arguments:
        - logger: The logger to use"""
        self._donor_entries: list[ReporterEntry[AddDonor]] = list()
        self._campaign_entries: list[ReporterEntry[AddCampaign]] = list()
        self._donation_entries: list[ReporterEntry[AddDonation]] = list()
        self._input_entries: list[ReporterEntry[str]] = list()
        self.logger = logger

    def report_success_donation(self, add_donation: AddDonation):
        """
            Adds a ReporterEntry with status of SUCCESS to donation's collection

            Keyword arguments:

            - add_donation -- target of the new ReporterEntry
        """
        self._donation_entries.append(ReporterEntry(result_type=ReporterEntryStatus.SUCCESS, target=add_donation, description=""))

    def report_skipped_donation(self, add_donation: AddDonation, description:str=""):
        """
            Adds a ReporterEntry with status of SKIPPED to donation's collection

            Keyword arguments:

            - add_donation -- target of the new ReporterEntry
            - description -- optional string describing this entry
        """
        self._donation_entries.append(ReporterEntry(result_type=ReporterEntryStatus.SKIPPED, description=description, target=add_donation))
        
        if self.logger:
            self.logger.warning(description)

    def report_error_donation(self, add_donation: AddDonation, description:str=""):
        """
            Adds a ReporterEntry with status of ERROR to donation's collection

            Keyword arguments:

            - add_donation -- target of the new ReporterEntry
            - description -- optional string describing this entry
        """
        self._donation_entries.append(ReporterEntry(result_type=ReporterEntryStatus.ERROR, description=description, target=add_donation))
        
        if self.logger:
            self.logger.error(description)
        
    def report_success_donor(self, add_donor: AddDonor):
        """
            Adds a ReporterEntry with status of SUCCESS to donor's collection

            Keyword arguments:

            - add_donor -- target of the new ReporterEntry
        """
        self._donor_entries.append(ReporterEntry(result_type=ReporterEntryStatus.SUCCESS, target=add_donor, description=""))

    def report_skipped_donor(self, add_donor: AddDonor, description:str=""):
        """
            Adds a ReporterEntry with status of SKIPPED to donor's collection

            Keyword arguments:

            - add_donor -- target of the new ReporterEntry
            - description -- optional string describing this entry
        """
        self._donor_entries.append(ReporterEntry(result_type=ReporterEntryStatus.SKIPPED, description=description, target=add_donor))
        
        if self.logger:
            self.logger.warning(description)

    def report_error_donor(self, add_donor: AddDonor, description:str=""):
        """
            Adds a ReporterEntry with status of ERROR to donor's collection

            Keyword arguments:

            - add_donor -- target of the new ReporterEntry
            - description -- optional string describing this entry
        """
        self._donor_entries.append(ReporterEntry(result_type=ReporterEntryStatus.ERROR, description=description, target=add_donor))
        
        if self.logger:
            self.logger.error(description)

    def report_success_campaign(self, add_campaign: AddCampaign):
        """
            Adds a ReporterEntry with status of SUCCESS to campaign's collection

            Keyword arguments:

            - add_campaign -- target of the new ReporterEntry
        """
        self._campaign_entries.append(ReporterEntry(result_type=ReporterEntryStatus.SUCCESS, target=add_campaign, description=""))

    def report_skipped_campaign(self, add_campaign: AddCampaign, description:str=""):
        """
            Adds a ReporterEntry with status of SKIPPED to campaign's collection

            Keyword arguments:

            - add_campaign -- target of the new ReporterEntry
            - description -- optional string describing this entry
        """
        self._campaign_entries.append(ReporterEntry(result_type=ReporterEntryStatus.SKIPPED, description=description, target=add_campaign))
        
        if self.logger:
            self.logger.warning(description)

    def report_error_campaign(self, add_campaign: AddCampaign, description:str=""):
        """
            Adds a ReporterEntry with status of ERROR to campaign's collection

            Keyword arguments:

            - add_campaign -- target of the new ReporterEntry
            - description -- optional string describing this entry
        """
        self._campaign_entries.append(ReporterEntry(result_type=ReporterEntryStatus.ERROR, description=description, target=add_campaign))
        
        if self.logger:
            self.logger.error(description)

    def report_success_input(self, line: str):
        """
            Adds a ReporterEntry with status of SUCCESS to input's collection

            Keyword arguments:

            - line -- target of the new ReporterEntry
        """
        self._input_entries.append(ReporterEntry(result_type=ReporterEntryStatus.SUCCESS, target=line, description=""))

    def report_skipped_input(self, line: str, description:str=""):
        """
            Adds a ReporterEntry with status of SKIPPED to input's collection

            Keyword arguments:

            - line -- target of the new ReporterEntry
            - description -- optional string describing this entry
        """
        self._input_entries.append(ReporterEntry(result_type=ReporterEntryStatus.SKIPPED, description=description, target=line))
        
        if self.logger:
            self.logger.warning(description)

    def report_error_input(self, line: str, description:str=""):
        """
            Adds a ReporterEntry with status of ERROR to input's collection

            Keyword arguments:

            - line -- target of the new ReporterEntry
            - description -- optional string describing this entry
        """
        self._input_entries.append(ReporterEntry(result_type=ReporterEntryStatus.ERROR, description=description, target=line))
        
        if self.logger:
            self.logger.error(description)

    def to_json_obj(self):
        """ Returns a string with a JSON representation of this object and it's relevant information"""
        dict_attributes:Dict[str,list[ReporterEntry]] = { key:value for key, value in self.__dict__.items() if value and not isinstance(value, logging.Logger)}
        return {key.removeprefix('_'):[internal_value.to_json_obj() for internal_value in value] for key, value in dict_attributes.items() if len(value)}
    