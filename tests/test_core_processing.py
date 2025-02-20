import json
import pytest

from internal.commands import AddCampaign, AddDonation, AddDonor
from internal.consolidator import Consolidator
from internal.core_processing import create_recurring_report_from, extract_command, process_command_line
from internal.entry_reporter import EntriesReporter, ReporterEntryStatus
from internal.models import Campaign, Donation, DonationFrequency, Donor


###
## EXTRACT GENERAL COMMANDS
###

@pytest.mark.parametrize('line', ["", None, "saraza", "saraza saraza sarazam ", "               "])
def test_bad_string(line):
    assert  extract_command(line) is None

###
## EXTRACT DONOR COMMANDS
###

@pytest.mark.parametrize('line', ["Add", "add DONOR", "ADD DONOR PEPE", "Add donor 1505           "])
def test_bad_command_add_donor(line):
    assert extract_command(line) is None

@pytest.mark.parametrize('line', ["Add donor pepe 0           ", "add donor pepe -1"])
def test_invalid_command_add_donor(line):
    assert extract_command(line) is None


@pytest.mark.parametrize('line', ["add donor pepe as10"])
def test_throws_exception_command_add_donor(line):
    
    with pytest.raises(ValueError) as excinfo:  
        extract_command(line)
    assert str(excinfo.value) == f"could not convert string to float: '{line.split()[::-1][0]}'" 


add_donor_success_params = [(f"add donor {donor.name} {donor.amount}", donor) for donor in [AddDonor(name="pepepe", amount=1), AddDonor(name="1515", amount=100)]]
@pytest.mark.parametrize('line, expected_result', add_donor_success_params)
def test_good_command_add_donor(line:str, expected_result:AddDonor):
    command = extract_command(line)
    assert isinstance(command, AddDonor)
    assert command.name == expected_result.name
    assert command.amount == expected_result.amount

add_donor_success_params = [(f"add donor {donor.name} ${donor.amount}", donor) for donor in [AddDonor(name="pepepe", amount=1), AddDonor(name="1515", amount=100)]]
@pytest.mark.parametrize('line, expected_result', add_donor_success_params)
def test_good_command_dollar_prefix_add_donor(line:str, expected_result:AddDonor):
    command = extract_command(line)
    assert isinstance(command, AddDonor)
    assert command.name == expected_result.name
    assert command.amount == expected_result.amount

###
## EXTRACT CAMPAIGN COMMANDS
###

@pytest.mark.parametrize('line', ["Add", "add CAMPAIGN"])
def test_bad_command_add_campaign(line):
    assert extract_command(line) is None


add_campaign_success_params = [(f"add CAMPAIGN {campaign.name} ", campaign) for campaign in [AddCampaign(name="pepepe"), AddCampaign(name="1515")]]
@pytest.mark.parametrize('line, expected_result', add_campaign_success_params)
def test_good_command_add_campaign(line:str, expected_result:AddCampaign):
    command = extract_command(line)
    assert isinstance(command, AddCampaign)
    assert command.name == expected_result.name

###
## EXTRACT DONATION COMMANDS
###
@pytest.mark.parametrize('line', ["DONATE", "DONATE PEPE", "donate pepe WEEKLY pompin", "donate pepe WEEKLY pompin -1", "donate pepe WEEKLY otherPepe  0"])
def test_bad_command_add_donation(line):
    assert extract_command(line) is None

@pytest.mark.parametrize('line', ["dOnate pepe WEEKLY pompin 0           ", "dOnate pepe monthly pompin -1"])
def test_invalid_command_add_donation(line):
    assert extract_command(line) is None


@pytest.mark.parametrize('line', ["dOnate pepe A pompin  as10", "dOnate pepe badFrequency pompin  as10", "dOnate pepe Weeklyyy pompin  as10","dOnate pepe A pompin  as10", "dOnate pepe weekly pompin  as10", "dOnate pepe monthly pompin  as10"])
def test_throws_exception_command_add_donation(line):
    
    with pytest.raises(ValueError) as excinfo:  
        extract_command(line)
        assert 1 == len([msg for msg in [f"could not convert string to float: '{line.split()[::-1][0]}'", f"ValueError: '{line.split()[::][0]}' is not a valid DonationFrequency"] if msg == str(excinfo.value)])


add_donation_success_params = [(f"dOnate {donation.donor_name} {donation.frequency._value_} {donation.campaign_name} {donation.amount}", donation) for donation in [AddDonation(campaign_name="pepe", frequency=DonationFrequency.MONTHLY, donor_name="pompin", amount=1), AddDonation(campaign_name="1515", frequency=DonationFrequency.MONTHLY, donor_name="5468", amount=100)]]
@pytest.mark.parametrize('line, expected_result', add_donation_success_params)
def test_good_command_add_donation(line:str, expected_result:AddDonation):
    command = extract_command(line)
    assert isinstance(command, AddDonation)
    assert command.donor_name == expected_result.donor_name
    assert command.campaign_name == expected_result.campaign_name
    assert command.amount == expected_result.amount
    assert command.frequency == expected_result.frequency


add_donation_success_params = [(f"dOnate {donation.donor_name} {donation.frequency._value_} {donation.campaign_name} ${donation.amount}", donation) for donation in [AddDonation(campaign_name="pepe", frequency=DonationFrequency.MONTHLY, donor_name="pompin", amount=1), AddDonation(campaign_name="1515", frequency=DonationFrequency.MONTHLY, donor_name="5468", amount=100)]]
@pytest.mark.parametrize('line, expected_result', add_donation_success_params)
def test_good_command_dollar_prefix_add_donation(line:str, expected_result:AddDonation):
    command = extract_command(line)
    assert isinstance(command, AddDonation)
    assert command.donor_name == expected_result.donor_name
    assert command.campaign_name == expected_result.campaign_name
    assert command.amount == expected_result.amount

###
# RECURRING REPORT
###

def consolidator_modifier(consolidator:Consolidator, donors:list[Donor], campaigns:list[Campaign]):
    if len(donors):
        consolidator._donors = {donor.key: donor for donor in donors}
    
    if len(campaigns):
        consolidator._campaigns = {campaign.key: campaign for campaign in campaigns}

    return consolidator

test_donor = Donor("test_key", name="test_name",funds=136)
test_donor.donations.append(Donation(amount=25, frequency=DonationFrequency.MONTHLY, campaign_key="cASD"))
test_donor.donations.append(Donation(amount=55, frequency=DonationFrequency.MONTHLY, campaign_key="cASD"))

testing_consolidators_for_report = [
    (None, ""),
    (Consolidator(EntriesReporter(None)), ""),
    (consolidator_modifier(Consolidator(EntriesReporter(None)), [], []), ""),
    (consolidator_modifier(Consolidator(EntriesReporter(None)), [Donor(key="asf", name='ASD', funds=153)], []), 
     '\n'.join(["Donors:", "ASD: Total: $0 Average: $0"])),
    (consolidator_modifier(Consolidator(EntriesReporter(None)), [], [Campaign(key="casf", name='cASD', funds=1153)]), 
     '\n'.join(["Campaigns:", "cASD: Total: $1153"])),
    (consolidator_modifier(Consolidator(EntriesReporter(None)), [Donor(key="2asf", name='2ASD', funds=253), test_donor], [Campaign(key="2casf", name='2cASD', funds=2153)]), 
     '\n'.join(["Donors:","2ASD: Total: $0 Average: $0", "test_name: Total: $80 Average: $40.0", "", "Campaigns:", "2cASD: Total: $2153"]))
    ]
@pytest.mark.parametrize('consolidator, expected_result', testing_consolidators_for_report)
def test_create_recurring_report(consolidator, expected_result):
    process_result = create_recurring_report_from(consolidator)
    assert process_result == expected_result


###
# PROCESS COMMAND LINE
###

def test_process_command_line_success():
    consolidator = Consolidator(EntriesReporter(None))
    line="add donor joselo 100"
    
    process_command_line(consolidator=consolidator, reporter=consolidator._reporter, line=line)

    assert len(consolidator.all_donors) == 1

    try:
        json_obj = consolidator._reporter.to_json_obj()
        json.dumps(json_obj)

        assert len(json_obj.get('donor_entries')) == 1
        
        assert json_obj.get('donor_entries')[0].get("result_type") == ReporterEntryStatus.SUCCESS
    except Exception as exc:
        assert False, str(exc)

def test_process_command_line_skipp():
    consolidator = Consolidator(EntriesReporter(None))
    line="add donor joselo -100"
    
    process_command_line(consolidator=consolidator, reporter=consolidator._reporter, line=line)

    assert len(consolidator.all_donors) == 0

    try:
        json_obj = consolidator._reporter.to_json_obj()
        json.dumps(json_obj)

        assert len(json_obj.get('input_entries')) == 1
        
        assert json_obj.get('input_entries')[0].get("result_type") == ReporterEntryStatus.SKIPPED
    except Exception as exc:
        assert False, str(exc)


def test_process_command_line_error():
    consolidator = Consolidator(EntriesReporter(None))
    line="add donor joselo 10asdf0"
    
    process_command_line(consolidator=consolidator, reporter=consolidator._reporter, line=line)

    assert len(consolidator.all_donors) == 0

    try:
        json_obj = consolidator._reporter.to_json_obj()
        json.dumps(json_obj)

        assert len(json_obj.get('input_entries')) == 1
        
        assert json_obj.get('input_entries')[0].get("result_type") == ReporterEntryStatus.ERROR
    except Exception as exc:
        assert False, str(exc)