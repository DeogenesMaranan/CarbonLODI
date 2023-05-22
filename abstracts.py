from abc import ABC, abstractmethod

class ErrorHandlerABC(ABC):
    """Abstract base class for error handling methods. """

    @abstractmethod
    def get_valid_option(self, prompt, valid_options):
        """Prompt the user for input and validate it against a list of valid options. 

        Args:
            prompt (str): The prompt message to display.
            valid_options (list): List of valid options.

        Returns:
            str: The user's valid input option.
        """
        pass

    @abstractmethod
    def get_float(self, prompt):
        """Prompt the user for a float value.

        Args:
            prompt (str): The prompt message to display. 

        Returns:
            float: The user's input value.
        """
        pass

    @abstractmethod
    def get_int(self, prompt):
        """Prompt the user for an integer value. 

        Args:
            prompt (str): The prompt message to display.

        Returns:
            int: The user's input value.
        """
        pass


class CarbonCalculatorABC(ErrorHandlerABC, ABC):
    """Abstract base class for carbon calculator methods."""

    @abstractmethod
    def calculate_housing_emissions(self):
        """Calculate housing emissions based on user input.

        Returns:
            float: The calculated housing emissions.
        """
        pass

    @abstractmethod
    def calculate_transportation_emissions(self):
        """Calculate transportation emissions based on user input.

        Returns:
            float: The calculated transportation emissions.
        """
        pass

    @abstractmethod
    def calculate_food_emissions(self):
        """Calculate food emissions based on user input.

        Returns:
            float: The calculated food emissions.
        """
        pass

    @abstractmethod
    def calculate_all(self, current_user):
        """Calculate total carbon emissions for all categories and store the result.

        Args:
            current_user (str): The current user's name.
        """
        pass


class AccountManagerABC(CarbonCalculatorABC, ABC):
    """Abstract base class for account management methods."""

    @abstractmethod
    def register(self):
        """Register a new user account."""
        pass

    @abstractmethod
    def load_users(self):
        """Load user account information."""
        pass

    @abstractmethod
    def login(self):
        """Prompt the user to login."""
        pass

    @staticmethod
    @abstractmethod
    def file_to_dict(current_user):
        """Convert a file to a dictionary.

        Args:
            current_user (str): The current user's name.

        Returns:
            dict: The converted dictionary.
        """
        pass

    @staticmethod
    @abstractmethod
    def generate_table(data_dict):
        """Generate a table from a dictionary.

        Args:
            data_dict (dict): The data dictionary.

        Returns:
            str: The generated table.
        """
        pass

    @abstractmethod
    def show_home(self, current_user):
        """Display the home screen for the logged-in user.

        Args:
            current_user (str): The current user's name.
        """
        pass
