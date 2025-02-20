
import json
from typing import Dict
from internal.commands import AddCampaign, AddDonation, AddDonor, CommandExecutor
from internal.models import Campaign, Donation, Donor
from internal.entry_reporter import EntriesReporter


class Consolidator(CommandExecutor):
    """Consolidator is a class that encapsulates domain objects (Donors and Campaigns) and also holds
       a EntriesReporter that will log the processing result of each one of the commands we receive.
    """
    def __init__(self, reporter:EntriesReporter):
        """
            Constructor for this class.

            Keyword arguments:
            reporter -- EntriesReporter instance
        """
        self._donors:Dict[str,Donor] = dict()
        self._campaigns:Dict[str,Campaign] = dict()
        self._reporter = reporter
    
    @property
    def all_donors(self) -> list[Donor]:
        """Returns a copy of the donors list currently in the system."""
        return list(self._donors.values())

    @property
    def all_campaigns(self) -> list[Campaign]:
        """Returns a copy of the campaigns list currently in the system."""
        return list(self._campaigns.values())

    def has_any_data(self):
        """Returns a boolean indicating if the consolidator holds some data as result of the processing of commands.

            returns bool
        """
        return bool(len(self._donors) or len(self._campaigns))

    def accept_donation(self, donation: AddDonation):
        """ Executes a command syncying the contents of the models to its effects as it creates entries in reporter for the processing of the command.

            Keyword arguments:
            donation -- command that holds data for executing the donation
        """
        if not self._donors.get(donation.donor_name.lower()):
            self._reporter.report_skipped_donation(donation, f"Unable to find donor with key: {donation.donor_name.lower()} while trying to process donation")
            return
            
        if not self._campaigns.get(donation.campaign_name.lower()):
            self._reporter.report_skipped_donation(donation, f"Unable to find campaign with key: {donation.donor_name.lower()} while trying to process donation")
            return

        if not donation.validate():
            self._reporter.report_skipped_donation(donation, f"Invalid donation from: {donation.donor_name.lower()} to: {donation.campaign_name.lower()} with amount: {str(donation.amount)}")
            return

        donor = self._donors[donation.donor_name.lower()]
        campaign = self._campaigns[donation.campaign_name.lower()]

        total_donation_amount = donation.get_donation_amount()
        if donor.funds < total_donation_amount:
            self._reporter.report_skipped_donation(donation, f"Donation funds ({str(total_donation_amount)}) exceeds donor funds ({str(donor.funds)})")
        else:
            campaign.funds += total_donation_amount
            donor.funds -= total_donation_amount
            donor.donations.append(Donation(campaign_key=donation.campaign_name.lower(), frequency=donation.frequency, amount=donation.amount))

            self._reporter.report_success_donation(donation)

    def accept_donor(self, add_donor: AddDonor):
        """ Executes a command syncying the contents of the models to its effects as it creates entries in reporter for the processing of the command.

            Keyword arguments:
            add_donor -- command that holds data for creating a donor
        """
        if not add_donor.validate():
            self._reporter.report_skipped_donation(add_donor, f"Invalid donor: {add_donor.name} with amount: {str(add_donor.amount)}")
            return
        
        if not self._donors.get(add_donor.name.lower(), None):

            self._donors[add_donor.name.lower()] = Donor(add_donor.name.lower(), add_donor.name, add_donor.amount)
            self._reporter.report_success_donor(add_donor)
        else:
            self._reporter.report_skipped_donor(add_donor, f"Ignoring donor with key: {add_donor.name.lower()} since it already exists another donor for the same key")
            return

    def accept_campaign(self, add_campaign: AddCampaign):
        """ Executes a command syncying the contents of the models to its effects as it creates entries in reporter for the processing of the command.

            Keyword arguments:
            add_campaign -- command that holds data for creating a campaign
        """
        if not add_campaign.validate():
            self._reporter.report_skipped_donation(add_campaign, f"Invalid donor: {add_campaign.name}")
            return

        if not self._campaigns.get(add_campaign.name.lower(), None):
            self._campaigns[add_campaign.name.lower()] = Campaign(add_campaign.name.lower(), add_campaign.name, 0)
            self._reporter.report_success_campaign(add_campaign)
        else:
            self._reporter.report_skipped_campaign(add_campaign, f"Ignoring campaign with key: {add_campaign.name.lower()} since it already exists another campaign for the same key")
            return

    def to_json(self):
        """ Returns a string with a JSON representation of this object and it's relevant information"""

        return json.dumps({
            "donors": dict([(key, value.to_json_obj()) for key, value in self._donors.items()]),
            "campaigns": dict([(key, value.to_json_obj()) for key, value in self._campaigns.items()]),
            "report": self._reporter.to_json_obj()
            }, indent=4)