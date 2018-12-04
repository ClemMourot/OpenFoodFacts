from constants import *


def replace_product(connection, cursor):

    on = True

    while on:

        print("Trouver un substitut")
        print("\n")
        print("Sélectionnez la catégorie :")
        print("\n")

        get_categories = ("SELECT name FROM categories")

        cursor.execute(get_categories)

        for idx, category in enumerate(cursor, 1):
            print(idx, "-", category)

        print("\n")

        try:
            choice = int(input())
            if choice < 0 or choice > categories_nb:
                str(choice)

        except ValueError:
            continue

        print("\n")

        print("Sélectionnez l'aliment")

        print("\n")

        get_products = ("SELECT name FROM products "
                 "WHERE category_id = %s")

        cursor.execute(get_products, choice)

        for idx, product in enumerate(cursor, 1):
            print(idx, "-", product)

        print("\n")

        try:
            choice = int(input())
            if choice < 0 or choice > idx:
                pass

        except ValueError:
            continue

        print("\n")

        connection.commit()


def substitutes_display(connection, cursor):

    on = True

    while on:

        print("Mes aliments substitués")

        """for idx, substitute in enumerate(substitutes_list, 1):
            print(idx, "-", substitutes_list[idx].name)"""

        get_substitutes = ("SELECT name FROM products "
                 "WHERE saved = '1'")

        cursor.execute(get_substitutes)

        for idx, substitute in enumerate(cursor, 1):
            print(idx, "-", substitute)

        print("\n")

        try:
            choice = int(input())
            if choice < 0 or choice > idx:
                pass

        except ValueError:
            continue

        print("\n")

        connection.commit()
