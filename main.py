import os
import time
import sys
try:
    from miscellaneous import Constants
    from miscellaneous import AccountManager
except ModuleNotFoundError:  # Handle the missing module error
    print("The 'miscellaneous.py' file is missing.")
    print("Please download the latest version of the Repository")
    time.sleep(3)
    sys.exit(1002)

def main():
    """
    Displays a menu to the user and handles user choices.

    The function presents a menu to the user, clears the screen, and processes the user's choice.
    It supports user registration, login, and exiting the program.

    note: Converting this while loop into a function allows it to be called from other files, such as Jupyter Notebooks, even though it may be more concise and functional without making it 
    a separate function.
    """
    while True:  # Runs the Main Menu in loop
        os.system('cls')
        print(Constants().logo)
        Constants.print_random_recommendation()
        choice = input(Constants().main_menu)
        print("")

        os.system('cls')  # Clear the screen before processing user choice 

        if choice == '1':
            print(f"{Constants().logo}")
            Constants.print_random_recommendation()
            print("")
            current_user = AccountManager().register()
            input("\nPress any key to continue...")
        elif choice == '2':
            print(Constants.logo)
            Constants.print_random_recommendation()
            print("")
            current_user = AccountManager().login()
            if current_user is None:
                input("\nPress any key to continue...")
            else:
                AccountManager().show_home(current_user)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

main()
