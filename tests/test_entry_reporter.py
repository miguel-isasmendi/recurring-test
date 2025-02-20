import logging
import pytest

from internal.commands import AddCampaign, AddDonation, AddDonor
from internal.entry_reporter import EntriesReporter, ReporterEntryStatus
from internal.models import DonationFrequency

###
## CONSTRUCTOR
###

@pytest.mark.parametrize('logger', [None, logging.getLogger("test")])
def test_constructor_entries_reporter(logger):
    try:
        EntriesReporter(logger)
    except:
        assert False , f"Unable to instantiate EntriesReporter"
###
# General
###

def _do_test_reporting(logger, lambda_executor, json_key, expected_status: ReporterEntryStatus):
    reporter = EntriesReporter(logger)
    try:
        lambda_executor(reporter)
        assert len(reporter.to_json_obj()[json_key]) == 1
        assert reporter.to_json_obj()[json_key][0]["result_type"] == expected_status
    except:
        assert False , f"Unable to report target"

###
## Donor reporting
###
report_parameters_donor = [(None, AddDonor(name="test", amount=10)), (logging.getLogger("test"), AddDonor(name="test", amount=10))]

@pytest.mark.parametrize('logger, target', report_parameters_donor)
def test_reporter_donor_success(logger, target):
    _do_test_reporting(logger=logger,
                       lambda_executor=lambda reporter: reporter.report_success_donor(target) ,
                       json_key="donor_entries",
                       expected_status=ReporterEntryStatus.SUCCESS)

@pytest.mark.parametrize('logger, target', report_parameters_donor)
def test_reporter_donor_skipped(logger, target):
    _do_test_reporting(logger=logger,
                       lambda_executor=lambda reporter: reporter.report_skipped_donor(target, "description") ,
                       json_key="donor_entries",
                       expected_status=ReporterEntryStatus.SKIPPED)

@pytest.mark.parametrize('logger, target', report_parameters_donor)
def test_reporter_donor_error(logger, target):
    _do_test_reporting(logger=logger,
                       lambda_executor=lambda reporter: reporter.report_error_donor(target, "description") ,
                       json_key="donor_entries",
                       expected_status=ReporterEntryStatus.ERROR)


###
## Campaign reporting
###
report_parameters_campaign = [(None, AddCampaign(name="test")), (logging.getLogger("test"), AddCampaign(name="test"))]

@pytest.mark.parametrize('logger, target', report_parameters_campaign)
def test_reporter_campaign_success(logger, target):
    _do_test_reporting(logger=logger,
                       lambda_executor=lambda reporter: reporter.report_success_campaign(target) ,
                       json_key="campaign_entries",
                       expected_status=ReporterEntryStatus.SUCCESS)

@pytest.mark.parametrize('logger, target', report_parameters_campaign)
def test_reporter_campaign_skipped(logger, target):
    _do_test_reporting(logger=logger,
                       lambda_executor=lambda reporter: reporter.report_skipped_campaign(target, "description") ,
                       json_key="campaign_entries",
                       expected_status=ReporterEntryStatus.SKIPPED)

@pytest.mark.parametrize('logger, target', report_parameters_campaign)
def test_reporter_campaign_error(logger, target):
    _do_test_reporting(logger=logger,
                       lambda_executor=lambda reporter: reporter.report_error_campaign(target, "description") ,
                       json_key="campaign_entries",
                       expected_status=ReporterEntryStatus.ERROR)

###
## Donation reporting
###
report_parameters_donation = [(None, AddDonation(donor_name="pepe", frequency=DonationFrequency.MONTHLY, campaign_name="wut", amount=15)), (logging.getLogger("test"), AddDonation(donor_name="pepe", frequency=DonationFrequency.MONTHLY, campaign_name="wut", amount=15))]

@pytest.mark.parametrize('logger, target', report_parameters_donation)
def test_reporter_donation_success(logger, target):
    _do_test_reporting(logger=logger,
                       lambda_executor=lambda reporter: reporter.report_success_donation(target) ,
                       json_key="donation_entries",
                       expected_status=ReporterEntryStatus.SUCCESS)

@pytest.mark.parametrize('logger, target', report_parameters_donation)
def test_reporter_donation_skipped(logger, target):
    _do_test_reporting(logger=logger,
                       lambda_executor=lambda reporter: reporter.report_skipped_donation(target, "description") ,
                       json_key="donation_entries",
                       expected_status=ReporterEntryStatus.SKIPPED)

@pytest.mark.parametrize('logger, target', report_parameters_donation)
def test_reporter_donation_error(logger, target):
    _do_test_reporting(logger=logger,
                       lambda_executor=lambda reporter: reporter.report_error_donation(target, "description") ,
                       json_key="donation_entries",
                       expected_status=ReporterEntryStatus.ERROR)
    
###
## Input reporting
###
report_parameters_input = [(None, "Add donor pepe 15"), (logging.getLogger("test"), "Add donor pepe 15")]

@pytest.mark.parametrize('logger, target', report_parameters_input)
def test_reporter_input_success(logger, target):
    _do_test_reporting(logger=logger,
                       lambda_executor=lambda reporter: reporter.report_success_input(target) ,
                       json_key="input_entries",
                       expected_status=ReporterEntryStatus.SUCCESS)

@pytest.mark.parametrize('logger, target', report_parameters_input)
def test_reporter_input_skipped(logger, target):
    _do_test_reporting(logger=logger,
                       lambda_executor=lambda reporter: reporter.report_skipped_input(target, "description") ,
                       json_key="input_entries",
                       expected_status=ReporterEntryStatus.SKIPPED)

@pytest.mark.parametrize('logger, target', report_parameters_input)
def test_reporter_input_error(logger, target):
    _do_test_reporting(logger=logger,
                       lambda_executor=lambda reporter: reporter.report_error_input(target, "description") ,
                       json_key="input_entries",
                       expected_status=ReporterEntryStatus.ERROR)