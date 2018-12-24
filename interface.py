import get_data
import database_access
from database_class import *


def menu():
    """displays the menu and returns the user's choice"""

    print("\n")
    print("    MENU    ")
    print("\n")
    print("1 - Remplacer un aliment")
    print("2 - Retrouver mes aliments substitués")
    print("3 - Quitter")
    print("\n")

    choice = int(input())

    return choice


def program():
    """initializes Database object and MySQL connection
    and runs the function needed based on the user's menu choice"""

    database = Database()  # instantiates Database object

    get_data.insert_into_database(database, database.connection,
                                  database.cursor)
    # gathers and inserts data into MySQL database

    on = True

    while on:  # until the user chooses to exit the program

        try:

            choice = menu()

            if choice <= 0 or choice > 3:

                pass

        except ValueError:

            continue

        if choice == 1:

            print("\n")
            database_access.replace_product(database.cursor,
                                            database.connection)
            # user chose to replace an item

        if choice == 2:

            print("\n")
            database_access.substitutes_display(database.cursor,
                                                database.connection)
            # user chose to access his already saved substitutes

        if choice == 3:  # user chose to quit the program

            on = False

    database.connection.close()


program()
