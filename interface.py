from constants import *


def replace_product():
    print("Trouver un substitut")
    print("Sélectionnez la catégorie :")

    for idx, category in enumerate(categories_names_url, 1):
        print(idx, "-", category)


def get_substitutes():
    pass


def menu():
    on = True
    while on:
        print("1 - Quel aliment souhaitez-vous remplacer ?")
        print("2 - Retrouver mes aliments substitués")
        print("3 - Quitter")
        print("\n")

        choice = input()

        if choice == '1':
            replace_product()

        if choice == '2':
            get_substitutes()

        if choice == '3':
            on = False


menu()
