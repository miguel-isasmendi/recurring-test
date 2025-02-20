import json
import pytest

from internal.commands import AddCampaign, AddDonation, AddDonor, Command, CommandExecutor
from internal.models import DonationFrequency

class TestExecutor(CommandExecutor):
    __test__ = False
    def __init__(self):
        self.command_received_class=None

    def accept_donation(self, donation: AddDonation):
        self.command_received_class = AddDonation
    def accept_donor(self, add_donor: AddDonor):
        self.command_received_class = AddDonor
    def accept_campaign(self, add_campaign: AddCampaign):
        self.command_received_class = AddCampaign

###
## GENERAL COMMANDS
###

all_commands:list[Command]=[AddCampaign(name="asdf"), AddDonation(donor_name="test", frequency=DonationFrequency.MONTHLY, campaign_name="fasdf", amount=156), AddDonor(name="asdf", amount=546)]

@pytest.mark.parametrize('command', all_commands)
def test_validates_executor_dispatch(command):
    executor = TestExecutor()

    command.dispatch_to_executor(executor=executor)

    assert executor.command_received_class == command.__class__

@pytest.mark.parametrize('command', all_commands)
def test_validates_executor_dispatch(command):
    try:
        json_obj = command.to_json_obj()

        json.dumps(json_obj)
    except Exception as exc:
        assert False, str(exc)

###
## DONOR COMMANDS
###

commands_validates_true = [AddDonor(name="pepepe", amount=1), AddDonor(name="1515", amount=100)]
@pytest.mark.parametrize('command', commands_validates_true)
def test_validates_true_add_donor(command:AddDonor):
    assert command.validate()

commands_validates_false = [AddDonor(name="pepepe", amount=0), AddDonor(name=None, amount=None), AddDonor(name="", amount=100), AddDonor(name="pepe", amount=-100)]
@pytest.mark.parametrize('command', commands_validates_false)
def test_validates_false_add_donor(command:AddDonor):
    assert not command.validate()

###
## CAMPAIGN COMMANDS
###


commands_validates_true = [AddCampaign(name="pepepe"), AddCampaign(name="1515")]
@pytest.mark.parametrize('command', commands_validates_true)
def test_validates_true_add_campaign(command:AddCampaign):
    assert command.validate()

commands_validates_false = [AddCampaign(name=None), AddCampaign(name="")]
@pytest.mark.parametrize('command', commands_validates_false)
def test_validates_false_add_campaign(command:AddCampaign):
    assert not command.validate()

###
## DONATION COMMANDS
###

commands_validates_true = [AddDonation(campaign_name="pepe", frequency=DonationFrequency.MONTHLY, donor_name="pompin", amount=1), AddDonation(campaign_name="1515", frequency=DonationFrequency.MONTHLY, donor_name="5468", amount=100)]
@pytest.mark.parametrize('command', commands_validates_true)
def test_validates_true_add_donation(command:AddDonation):
    assert command.validate()

commands_validates_false = [
    AddDonation(campaign_name="pepe", frequency=DonationFrequency.WEEKLY, donor_name="pompin", amount=-1),
    AddDonation(campaign_name="1515", frequency=None, donor_name="5468", amount=0),
    AddDonation(campaign_name=None, frequency=DonationFrequency.MONTHLY, donor_name="5468", amount=None),
    AddDonation(campaign_name=None, frequency=DonationFrequency.WEEKLY, donor_name="5468", amount=1),
    AddDonation(campaign_name="pepe", frequency=DonationFrequency.WEEKLY, donor_name=None, amount=None),
    AddDonation(campaign_name="pepe", frequency=DonationFrequency.WEEKLY, donor_name="5468", amount=None),
    AddDonation(campaign_name="pepe", frequency=DonationFrequency.WEEKLY, donor_name=None, amount=1),
    AddDonation(campaign_name="pepe", frequency=DonationFrequency.MONTHLY, donor_name="5468", amount=None),
    AddDonation(campaign_name="pepe", frequency=DonationFrequency.WEEKLY, donor_name=None, amount=1),
    AddDonation(campaign_name="pepe", frequency=None, donor_name="5468", amount=123)
]
@pytest.mark.parametrize('command', commands_validates_false)
def test_validates_false_add_donation(command:AddDonation):
    assert not command.validate()
