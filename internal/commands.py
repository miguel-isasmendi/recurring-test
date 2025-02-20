
from abc import abstractmethod
from enum import Enum
from typing import Generic, Self, TypeVar

from internal.models import DonationFrequency

AddDonation = TypeVar(Generic())
AddDonor = TypeVar(Generic())
AddCampaign = TypeVar(Generic())

class CommandExecutor(object):
    """Consolidator is an abstract class that defines the interface for the subclasses to accept different types of commands by its methods."""
    @abstractmethod
    def accept_donation(self, donation: AddDonation):
        """ Executes an AddDonation command.

            Keyword arguments:
            - donation -- command that holds data for executing the donation

            Returns None
        """
        pass

    @abstractmethod
    def accept_donor(self, add_donor: AddDonor):
        """ Executes an AddDonor command.

            Keyword arguments:
            - add_donor  -- command that holds data for creating a donor

            Returns None
        """
        pass

    @abstractmethod
    def accept_campaign(self, add_campaign: AddCampaign):
        """ Executes an AddCampaign command.

            Keyword arguments:
            - add_campaign --  command that holds data for creating a campaign

            Returns None
        """
        pass

class Command(object):
    index: int
    """
        Root abstract class for Commands that defines the interface for the subclasses to accept different types of commands by its methods. For the following purposes:

        - Being able to build and instance of itself from processing a string
        - Validate its content once instantiated
        - request a CommandExecutor to process the kind of command we are trying to execute.
        - create a json object representation of itself
    """
    @classmethod
    @abstractmethod
    def instantiate_from_string(cls, line:str) -> Self | None:
        """
            Method that creates an instance of the concret subclass parsing and processing the string received

            Keyword arguments:
            - line --  string that will be proceesed to create a subclass instance.

            Returns:
            An instance of a Command subclass or None
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """
            Method that is intended to validate the integrity and consistency of the data of the subclasses of this abstract class.

            Returns:
            bool
        """
        pass

    @abstractmethod
    def dispatch_to_executor(self, executor: CommandExecutor) -> None:
        """
            Method is intended to be overriten by subclasses to indicate the executor how to process this subclases

            Keyword arguments:
            - executor --  Command executor to which dispatch this command to be executed
        """
        pass
    
    def to_json_obj(self):
        """ Returns a string with a JSON representation of this object and it's relevant information"""
        return self.__dict__

class AddDonor(Command):
    """
        AddDonor implements Command's method signature, and holds variables that can be described as follows:

        - name: name of the donor
        - amount: amount of money this donor has initially
    """
    @classmethod
    def instantiate_from_string(cls, line:str) -> Command | None:
        """
            Class method that either returns an instance of this class or None in case we can't build an instance from the string received.

            A well formed string to create an instance has the following structure: `Add Donor <name> <amount>`
            Where:
            - the prefix `Add Donor` will be processed case insensitive
            - name will be stored as it is in name instance variable
            - amount can start with `$` prefix and it will be processed as long it can be parsed as float

            Keyword arguments:
            - line -- string to parse/process to create a new instance of this class

            Returns:
            - An instance of this class or None in case we can't build an instance from the string received.
        """
        prefix='add donor'

        if line and line.lower().startswith(prefix):
            params = line[len(prefix):].split()
            if len(params) > 1:
                name = params[0].strip()
                return AddDonor(name=name, amount=float(params[1].strip().removeprefix("$")))
            
        return None

    def __init__(self, name: str, amount: float):
        """
            Constructor for this class

            Keyword arguments:

            - name -- name of the donor
            - amount -- amount of money this donor has initially
        """

        self.name = name
        self.amount = amount

    def validate(self):
        """
            Validates to true if this instance has a name and amount, and amount is greater than 0

            Returns:
            bool
        """
        return bool(self.name and self.amount and self.amount > 0)
    
    
    def dispatch_to_executor(self, executor: CommandExecutor) -> None:
        """Dispatches itself to executor in the right method"""
        executor.accept_donor(self)

class AddCampaign(Command):
    """
        AddCampaign implements Command's method signature, and holds variables that can be described as follows:

        - name: name of the campaign
    """
    @classmethod
    def instantiate_from_string(cls, line:str) -> Command | None:
        """
            Class method that either returns an instance of this class or None in case we can't build an instance from the string received.

            A well formed string to create an instance has the following structure: `Add Campaign <name>`
            Where:
            - the prefix `Add Campaign` will be processed case insensitive
            - name will be stored as it is in name instance variable

            Keyword arguments:
            - line -- string to parse/process to create a new instance of this class

            Returns:
            - An instance of this class or None in case we can't build an instance from the string received.
        """

        prefix='add campaign'
        if line and line.lower().startswith(prefix):
            params = line[len(prefix):].split()
            if len(params):
                name = params[0].strip()
                return AddCampaign(name=name)
        else:
            return None
        
    def __init__(self, name: str):
        """
            Constructor for this class

            Keyword arguments:

            - name -- name of the donor
        """
        self.name = name

    def validate(self):
        """
            Validates to true if this instance has a name

            Returns:
            bool
        """
        return bool(self.name)
    
    def dispatch_to_executor(self, executor: CommandExecutor) -> None:
        """Dispatches itself to executor in the right method"""
        executor.accept_campaign(self)

class AddDonation(Command):
    """
        AddDonation implements Command's method signature, and holds variables that can be described as follows:

        - donor_name: name of the donor
        - campaign_name: name of the campaign
        - amount: amount of money to donate
    """
    @classmethod
    def instantiate_from_string(cls, line:str) -> Command | None:
        """
            Class method that either returns an instance of this class or None in case we can't build an instance from the string received.

            A well formed string to create an instance has the following structure: `Donate <donor_name> <campaign_name> <amount>`
            Where:
            - the prefix `Donate` will be processed case insensitive
            - donor_name will be stored as it is in name instance variable
            - frequency
            - campaign_name will be stored as it is in name instance variable
            - amount can start with `$` prefix and it will be processed as long it can be parsed as float

            Keyword arguments:
            - line -- string to parse/process to create a new instance of this class

            Returns:
            - An instance of this class or None in case we can't build an instance from the string received.
        """
        prefix = 'donate'
        if line and line.lower().startswith(prefix):
            params = line.lower().removeprefix(prefix).split()

            if len(params) > 3:
                return cls(
                    params[0].strip(),
                    DonationFrequency(params[1].upper()),
                    params[2].strip(),
                    float(params[3].strip().removeprefix("$")))
        
        return None

    def __init__(self, donor_name:str, frequency: DonationFrequency, campaign_name:str, amount: float):
        """
            Constructor for this class

            Keyword arguments:

            - donor_name -- name of the donor
            - campaign_name -- name of the campaign
            - frequency -- Enum with the frequency (MONTHLY, WEEKLY)
            - amount -- amount to donate
        """
        self.donor_name = donor_name
        self.campaign_name = campaign_name
        self.amount = amount
        self.frequency = frequency

    def get_donation_amount(self):
        final_amount = self.amount
        if self.frequency == DonationFrequency.WEEKLY:
            final_amount = final_amount * 4
        
        return final_amount


    def validate(self):
        """
            Validates to true if this instance has campaign_name, donor_name, amount, and amount is greater than 0

            Returns:
            bool
        """
        return bool(self.campaign_name and self.donor_name and self.frequency and self.amount and self.amount > 0)
    
    def dispatch_to_executor(self, executor: CommandExecutor) -> None:
        """Dispatches itself to executor in the right method"""
        executor.accept_donation(self)