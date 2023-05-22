import os
import time
import sys
try:
    from miscellaneous import Constants
    from miscellaneous import AccountManager
except ModuleNotFoundError:  # Handle the missing module error
    print("The 'miscellaneous.py' file is missing.")
    print("Please download the latest version of the Repository")
    time.sleep(4)
    sys.exit(1002)

while True:  # Runs the Main Menu in loop
    os.system('cls')
    print(Constants().logo)
    Constants.print_random_recommendation()
    choice = input(Constants().main_menu)
    print("")

    os.system('cls')  # Clear screen before processing user choice

    if choice == '1':
        current_user = AccountManager().register()
        input("\nPress any key to continue...")
    elif choice == '2':
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
