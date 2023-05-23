import time
import os
import sys
import datetime
import random

try:
    from tabulate import tabulate
except ModuleNotFoundError:
    # Handle the missing module error 
    print("The 'tabulate' module is not installed.")
    print("Please install it by running: pip install tabulate")
    time.sleep(3)
    sys.exit(1001)
try:
    from abstracts import ErrorHandlerABC
    from abstracts import CarbonCalculatorABC
    from abstracts import AccountManagerABC
except ModuleNotFoundError:
    # Handle the missing module error 
    print("The 'abstracts.py' file is missing.")
    print("Please download the latest version of the Repository")
    time.sleep(3)
    sys.exit(1002)


class Constants:
    """Store frequently used variables and method"""
    logo = '''

 ██████╗ █████╗ ██████╗ ██████╗  ██████╗ ███╗   ██╗    ██╗      ██████╗ ██████╗ ██╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔═══██╗████╗  ██║    ██║     ██╔═══██╗██╔══██╗██║
██║     ███████║██████╔╝██████╔╝██║   ██║██╔██╗ ██║    ██║     ██║   ██║██║  ██║██║
██║     ██╔══██║██╔══██╗██╔══██╗██║   ██║██║╚██╗██║    ██║     ██║   ██║██║  ██║██║
╚██████╗██║  ██║██║  ██║██████╔╝╚██████╔╝██║ ╚████║    ███████╗╚██████╔╝██████╔╝██║
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝    ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝'''

    main_menu = '''
                                     Main Menu
            
                                    1 - Register
                                    2 - Login
                                    0 - Exit
Response: '''

    home_menu = '''
                                        Menu

                                    1 - Calculate Emission
                                    2 - Track
                                    0 - Log out
Response: '''

    cooking_menu = '''
            Your cooking fuel
                0 - LPG
                1 - Electric
                2 - Bio

Response: '''

    transportation_menu = '''
                Your form of transportation 
                    0 - Walking
                    1 - Private Vehicle
                    2 - Public Vehicle

Response: '''

    @staticmethod
    def print_random_recommendation():
        """Prints random recommendation from '//resources/recommendations.txt' file"""
        file_path = os.path.join(os.getcwd(), 'resources', 'recommendations.txt')
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if lines:
                random_line = random.choice(lines)
                print(f"\nRecommendation: {random_line.strip()}")


class ErrorHandler(ErrorHandlerABC):
    def get_valid_option(self, prompt, valid_options=None):
        """Takes in string, returns whether the input is valid or not."""
        if valid_options is None:
            valid_options = ['0', '1', '2']
        while True:
            option = input(prompt)
            if option in valid_options:
                return option
            else:
                print(f"Invalid input.")

    def get_float(self, prompt):
        """Takes in positive float, returns whether the input is valid or not."""
        while True:
            try:
                value = float(input(prompt))
                if value > 0:
                    return value
                else:
                    print("Invalid input. Please enter a positive value.")
            except ValueError:
                print("Invalid input. Please enter a valid value.")

    def get_int(self, prompt):
        """Takes in positive int, returns whether the input is valid or not."""
        while True:
            try:
                value = int(input(prompt))
                if value > 0:
                    return value
                else:
                    print("Invalid input. Please enter a positive value.")
            except ValueError:
                print("Invalid input. Please enter a valid value.")

    def read_data_file(self, file_path):
        """Reads data from a file and converts it into a dictionary."""
        try:
            data = {}
            with open(file_path, 'r') as file:
                for line in file:
                    key, value = line.strip().split(' : ')
                    data[key] = value
            return data
        except FileNotFoundError:
            print(f"The file '{file_path}' is missing.")
            print("Please download the latest version of the Repository")
            time.sleep(3)
            sys.exit(1002)


class CarbonCalculator(CarbonCalculatorABC, ErrorHandler):
    """
    A class that calculates carbon emissions based on housing, transportation, and food information.
    Functions:
        calculate_housing_emissions(): Calculates carbon emissions from housing.
        calculate_transportation_emissions(): Calculates carbon emissions from transportation.
        calculate_food_emissions(): Calculates carbon emissions from food consumption.
        calculate_all(): Calculates total carbon emissions and provides recommendations.
    """

    def calculate_housing_emissions(self):  # Ask user for the housing information 
        """A prompt for collecting data from the housing emissions."""
        house_size_sq_m = self.get_float("Size of your house (square meters): ")
        occupants = self.get_int("Number of occupants in your house: ")
        electricity_use = self.get_float("Electric consumption per month (kWH): ")
        cooking_fuel = self.get_valid_option(Constants.cooking_menu)

        # Formulas for cooking per day
        if cooking_fuel == '0':
            cooking_emission = 35 / self.get_float("Estimate the number of days your 11 kg LPG lasts: ")
        elif cooking_fuel == '1':
            cooking_emission = self.get_float(
                "Estimate the average number of hours per day you use an electric stove: ") * 0.42
        else:
            cooking_emission = self.get_float(
                "Estimate the average number of hours per day you use a bio stove: ") * 0.03

        #  Formulas per month
        house_size_sq_ft = house_size_sq_m * 10.764  # 1 sq m = 10.764 sq ft 
        electricity_emissions = electricity_use * 0.5  # 0.5 kg CO2e per kWH

        # Convert to grams per day
        return ((electricity_emissions + cooking_emission) / occupants / house_size_sq_ft) * 1000 / 30

    def calculate_transportation_emissions(self):
        """A prompt for collecting data from the transportation emissions."""
        transportation_type = self.get_valid_option(Constants.transportation_menu)

        if transportation_type == '0':
            transportation_co2e = 0  # No emissions for walking
        elif transportation_type == '1':
            passengers = self.get_int("Number of people in the vehicle: ")
            distance = self.get_float("Distance of your transportation (km): ")
            fuel_efficiency = self.get_float(
                "What is the fuel efficiency of the vehicle (in km/L)? ")
            fuel_type = input("What type of fuel does the vehicle use? (1 - Gasoline / 2 - Diesel) ")
            emissions_factor = 2352.7 if fuel_type == '1' else 2639.4 if fuel_type == '2' else 0
            transportation_co2e = (emissions_factor * distance / fuel_efficiency) / passengers
        elif transportation_type == '2':
            distance = self.get_float("Distance of your transportation (km): ")
            transportation_co2e = 90 * distance  # 90 g CO2e/km/passenger on average for public transportation
        else:
            print("Sorry, we didn't understand your transportation type.")
            transportation_co2e = 0

        return transportation_co2e

    def calculate_food_emissions(self):
        """A prompt for collecting data from the food emissions."""
        emissions_dict = {}

        file_path = os.path.join(os.getcwd(), 'resources', 'food.txt')
        with open(file_path) as f:
            for line in f:
                food, emissions = line.strip().split(":")
                emissions_dict[food] = float(emissions)
        food_items = []
        while True:
            food_item = input("Enter a food item you ate today (or 'done' if finished): ")
            if food_item == 'done':
                break
            else:
                food_items.append(food_item)

        food_co2e = 0
        for food_item in food_items:
            if food_item in emissions_dict:
                servings = self.get_float(f"Your servings of {food_item} (grams) ")
                food_co2e += (servings * emissions_dict[food_item])
            else:
                print(f"Sorry, we don't have emissions data for {food_item}. Skipping...")
        return food_co2e

    def calculate_all(self, current_user):
        """Records the data into the designated text file."""
        date = datetime.datetime.now()
        total_emissions = self.calculate_housing_emissions() + self.calculate_transportation_emissions() + self.calculate_food_emissions()

        print(f"\nToday's total carbon emission is {round(total_emissions, 2)} grams")
        Constants.print_random_recommendation()
        file_path = os.path.join(os.getcwd(), 'users', f"user-{current_user}.txt")
        with open(file_path, 'a') as file:
            file.write(f"{date.strftime('%Y-%m-%d')} : {round(total_emissions, 2)}\n")


class AccountManager(AccountManagerABC, CarbonCalculator):
    """
    This is a Class for Account Managing.
    Functions:
        encrypt_password(password): (Private) Encrypts a password using a secret key. 
        register(): Prompts user for creating account info and stores it in 'users' dict and 'accounts.txt' file.
        load_users(): Loads user account information from the 'accounts.txt' file into the 'users' dict.
        login(): Prompts the user to login and checks if it matches a stored user account in the 'user' dict.
        file_to_dict(): Convert the 'user-username.txt' file into 'data_dict' dict.
        generate_table(): Convert 'data_dict' dict into a table using tabulate.
        show_home(): Prompts user a menu to choose from.
    """

    def __init__(self):
        self.current_user = None
        self.record = {}
        self.users = self.load_users

    @staticmethod
    def __encrypt_password(password):
        """(Private) Encrypts a password using a secret key."""
        __secret_key = "MathintheModernWorld"
        encrypted_password = ""
        for i, char in enumerate(password):  # Shifts each character by certain amount depending on the '__secret_key'
            shift = ord(__secret_key[i % len(__secret_key)]) - ord('a')
            shifted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            encrypted_password += shifted_char
        return encrypted_password

    @property
    def load_users(self):
        """Prompts user for creating account info and stores it in 'users' dict and 'accounts.txt' file."""
        file_path = os.path.join(os.getcwd(), 'resources', 'accounts.txt')
        try:
            users = {}
            with open(file_path, 'r') as file:
                for line in file:
                    username, encrypted_password = line.strip().split(':')
                    users[username] = {'password': encrypted_password}
            return users
        except FileNotFoundError:
            print("The 'accounts.txt' file is missing.")
            print("Please download the latest version of the Repository")
            time.sleep(3)
            sys.exit(1002)

    def register(self):
        """Prompts user for creating account info and stores it in 'users' dict and 'accounts.txt' file."""
        while True:
            username = input("Enter your username: ")
            if username in self.users:
                print("Username already exists. Please choose a different username.")
            else:
                break
        password = input("Enter a password: ")
        encrypted_password = self.__encrypt_password(password)
        self.users[username] = {'password': encrypted_password}
        file_path = os.path.join(os.getcwd(), 'resources', "accounts.txt")
        with open(file_path, 'a') as file:  # Appends every account into 'accounts.txt'
            file.write(f"{username}:{encrypted_password}\n")
        print("Registration successful.")
        return username

    def login(self):
        """Prompts the user to login and checks if it matches a stored user account in the 'user' dict. """
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        encrypted_password = self.__encrypt_password(password)
        if username in self.users and self.users[username]['password'] == encrypted_password:
            print(f"\nWelcome, {username}!")
            return username
        else:
            print("Invalid username or password..")

    @staticmethod
    def file_to_dict(current_user):
        """Convert the 'user-username.txt' file into 'data_dict' dict."""
        data_dict = {}
        try:
            file_path = os.path.join(os.getcwd(), 'users', f"user-{current_user}.txt")
            read_data_file(file_path)
        except FileNotFoundError:
            print(f"File 'user-{current_user}.txt' does not exist.")

    @staticmethod
    def generate_table(data_dict):
        """Convert 'data_dict' dict into a table using tabulate."""
        if not data_dict:
            print("Data dictionary is empty. File may not exist.")
            return ''

        table = []
        headers = ['Date', 'Total Emissions (grams)']
        for date, emissions in data_dict.items():
            table.append([date, emissions])
        return tabulate(table, headers, tablefmt='grid')

    def show_home(self, current_user):
        """Prompts user a menu to choose from."""
        self.current_user = current_user
        os.system('cls')
        print(Constants.logo)
        Constants.print_random_recommendation()
        choice = self.get_valid_option(Constants.home_menu)
        if choice == '1':
            self.calculate_all(self.current_user)
            input("\nPress any key to continue...")
            self.show_home(current_user)
        elif choice == '2':
            data_dict = self.file_to_dict(current_user)
            print(f"\n{self.generate_table(data_dict)}")
            Constants.print_random_recommendation()
            input("\nPress any key to continue...")
            self.show_home(current_user)
        else:
            pass
