from constants import *
from classes import *
import get_data


def replace_product(products_list):

    print("Trouver un substitut")
    print("\n")
    print("Sélectionnez la catégorie :")
    print("\n")

    for idx, category in enumerate(categories_names_url, 1):
        print(idx, "-", category)

    print("\n")

    choice = int(input())

    print("\n")

    print("Sélectionnez l'aliment")

    for idx, product in enumerate(products_list, 1):
        if product.category_id == choice:
            print(idx, "-", product.name)

    print("\n")

    choice = int(input())

    print("\n")

    print(products_list[choice].name)


def get_substitutes(substitutes_list):

    print("Mes aliments substitués")
    for idx, substitute in enumerate(substitutes_list, 1):
        print(idx, "-", substitutes_list[idx].name)

    print("\n")

    choice = int(input())

    print("\n")

    print(substitutes_list[choice].name)


def menu():

    print("1 - Remplacer un aliment")
    print("2 - Retrouver mes aliments substitués")
    print("3 - Quitter")
    print("\n")

    choice = input()

    return choice


def program():

    database = Database()
    get_data.insert_into_database(database)

    on = True
    while on:

        choice = menu()

        if choice == '1':
            print("\n")
            replace_product(database.products)

        if choice == '2':
            print("\n")
            get_substitutes(database.substitutes)

        if choice == '3':
            on = False


program()
