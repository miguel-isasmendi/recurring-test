from datetime import datetime, timezone
from enum import Enum

from internal.core import TIMESTAMP_FORMAT

class DonationFrequency(str, Enum):
    """Enum that represents the different status a ReporterEntry can be in a given time"""
    MONTHLY = "MONTHLY"
    WEEKLY = "WEEKLY"

class Model(object):
    def __init__(self):
        self.created: datetime = datetime.now(timezone.utc)

    def to_json_obj(self):
        """ Returns a JSON serializable object representation of this object and it's relevant information"""
        return { key: (value.strftime(TIMESTAMP_FORMAT) if isinstance(value, datetime) else value) for key, value in self.__dict__.items() }


class Donation(Model):
    def __init__(self, campaign_key:str, frequency:DonationFrequency, amount:float):
        super(Donation, self).__init__()
        self.campaign_key = campaign_key
        self.frequency = frequency
        self.amount=amount
        
    def get_donation_amount(self):
        final_amount = self.amount
        if self.frequency == DonationFrequency.WEEKLY:
            final_amount = final_amount * 4
        
        return final_amount

    
class Donor(Model):
    def __init__(self, key:str, name:str, funds:float):
        super(Donor, self).__init__()
        self.key = key
        self.name=name
        self.funds = funds
        self.donations:list[Donation] = list()

    def to_json_obj(self):
        """ Returns a JSON serializable object representation of this object and it's relevant information"""
        return { key: ([object.to_json_obj() for object in value] if isinstance(value, list) else (
                        value.strftime(TIMESTAMP_FORMAT) if isinstance(value, datetime) else value))
                        for key, value in self.__dict__.items() }

class Campaign(Model):
    def __init__(self, key:str, name:str, funds:float):
        super(Campaign, self).__init__()
        self.key = key
        self.name=name
        self.funds = funds