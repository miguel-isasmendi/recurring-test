
import json
import logging
import pytest

from internal.commands import AddCampaign, AddDonation, AddDonor, Command
from internal.consolidator import Consolidator
from internal.entry_reporter import EntriesReporter
from internal.models import Campaign, DonationFrequency, Donor

###
## CONSOLIDATOR CONSTRUCTOR
###

@pytest.mark.parametrize('consolidator', [Consolidator(EntriesReporter(None))])
def test_initial_data(consolidator):
    assert not len(consolidator.all_campaigns)
    assert not len(consolidator.all_donors)
    assert not consolidator.has_any_data()

###
## General
###

@pytest.mark.parametrize('commands', [[AddDonor(name="Pepe", amount=1563)],[AddCampaign(name="camp")]])
def test_has_any_data(commands):
    consolidator = Consolidator(EntriesReporter(logging.getLogger("test")))
    
    assert not consolidator.has_any_data()

    for command in commands:
        command.dispatch_to_executor(consolidator)

    assert consolidator.has_any_data()

@pytest.mark.parametrize('commands', [[AddDonor(name="Pepe", amount=1563),AddCampaign(name="camp")]])
def test_to_json(commands):
    consolidator = Consolidator(EntriesReporter(logging.getLogger("test")))
    
    assert not consolidator.has_any_data()

    for command in commands:
        command.dispatch_to_executor(consolidator)

    json_object = json.loads(consolidator.to_json())
    assert len(json_object["donors"]) == 1
    assert len(json_object["campaigns"]) == 1

###
## Dispatch commands
###

@pytest.mark.parametrize('commands',
                         [
                            [
                                AddDonor(name="Pepe", amount=1563),
                                AddCampaign(name="camp"),
                                AddDonation(campaign_name="camp", frequency=DonationFrequency.MONTHLY, donor_name="pepe", amount=563),
                                AddDonation(campaign_name="camp", frequency=DonationFrequency.MONTHLY, donor_name="pepe", amount=100)
                            ],
                            [
                                AddDonor(name="Pepe", amount=1563),
                                AddDonor(name="Pepe", amount=66666),
                                AddDonor(name="Pepe", amount=-1),
                                AddCampaign(name="camp"),
                                AddCampaign(name="camp"),
                                AddCampaign(name=""),
                                AddDonation(campaign_name="camp", frequency=DonationFrequency.MONTHLY, donor_name="pepe", amount=563),
                                AddDonation(campaign_name="camp", frequency=DonationFrequency.MONTHLY, donor_name="pepe", amount=-1),
                                AddDonation(campaign_name="camp", frequency=DonationFrequency.MONTHLY, donor_name="pepe", amount=100),
                                AddDonation(campaign_name="camp", frequency=DonationFrequency.MONTHLY, donor_name="pepe", amount=10000),
                                AddDonation(campaign_name="camp", frequency=DonationFrequency.MONTHLY, donor_name="unexistingPepe", amount=10000),
                                AddDonation(campaign_name="unexistingCamp", frequency=DonationFrequency.MONTHLY, donor_name="pepe", amount=10000),
                                AddDonation(campaign_name="unexistingCamp", frequency=DonationFrequency.MONTHLY, donor_name="unexistingPepe", amount=10000)
                            ]
                        ])
def test_dispatch(commands:list[Command]):
    consolidator = Consolidator(EntriesReporter(logging.getLogger("test")))

    assert not len(consolidator.all_donors)
    assert not len(consolidator.all_campaigns)
    assert not consolidator.has_any_data()

    for command in commands:
        command.dispatch_to_executor(consolidator)

    assert consolidator.has_any_data()
    assert len(consolidator.all_donors) == 1
    assert len(consolidator.all_donors[0].donations) == 2
    assert len(consolidator.all_campaigns) == 1
