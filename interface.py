from classes import *
import get_data
import database_access
import mysql.connector


def menu():

    print("\n")
    print("1 - Remplacer un aliment")
    print("2 - Retrouver mes aliments substitués")
    print("3 - Quitter")
    print("\n")

    choice = int(input())

    return choice


def program():

    database = Database()
    connection = mysql.connector.connect(user='user', database='open_food_facts')
    cursor = connection.cursor()
    #get_data.insert_into_database(database, connection, cursor)

    on = True
    while on:

        try:
            choice = menu()
            if choice < 0 or choice > 3:
                pass

        except ValueError:
            continue

        if choice == 1:
            print("\n")
            database_access.replace_product(connection, cursor)

        if choice == 2:
            print("\n")
            database_access.substitutes_display(connection, cursor)

        if choice == 3:
            on = False

    cursor.close()
    connection.close()


program()
