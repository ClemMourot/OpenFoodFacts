from constants import *


def categories_display(cursor):

    user_input = False

    while not user_input:

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
                pass
            else:
                return choice
                user_input = True
        except ValueError:
            continue


def products_display(cursor, choice):

    user_input = False

    while not user_input:

        print("\n")
        print("Sélectionnez l'aliment")

        get_products = ("SELECT name, p_id FROM products WHERE category_id = %d ") % choice
        cursor.execute(get_products)

        for idx, (name, p_id) in enumerate(cursor, 1):
            print(p_id, "-", name)

        print("\n")

        try:
            choice = int(input())
            if choice < 0 or choice > p_id:
                pass
            else:
                return choice
                user_input = True
        except ValueError:
            continue


def item_display(cursor, connection, choice):

    on = True
    while on:

        print("\n")
        print("Voici les détails de l'aliment choisi :")

        get_item = ("SELECT name, url, score, category_id FROM products WHERE p_id = %d") % choice
        cursor.execute(get_item)

        for idx, (name, url, p_score, category_id) in enumerate(cursor, 1):
            print(name, url, p_score, category_id)

        print("\n")
        print("Voici un substitut pour cet aliment :")

        get_substitute = ("SELECT name, url, score, p_id FROM products "
                          "WHERE score < %d AND p_id != %d AND category_id = %d LIMIT 1") % (p_score, choice, category_id)
        cursor.execute(get_substitute)

        for idx, (name, url, p_score, p_id) in enumerate(cursor, 1):
            print(name, url, p_score, p_id)

        print("\n")
        print("Appuyez sur 'S' pour sauvegarder cet aliment")

        wait = True
        while wait:
            key = input()
            if key == 'S':
                print("a")
                save_substitute = ("UPDATE products SET saved = '1' WHERE p_id = %d") % p_id
                cursor.execute(save_substitute)
                connection.commit()
                print("Appuyez sur 'E' pour retourner au menu")
            if key == 'E':
                wait = False
                on = False


def replace_product(cursor, connection):

    on = True

    while on:

        choice = categories_display(cursor)
        choice = products_display(cursor, choice)
        item_display(cursor, connection, choice)

        on = False


def substitutes_display(cursor, connection):

    on = True

    while on:

        print("Mes aliments substitués")

        get_substitutes = ("SELECT name FROM products WHERE saved = '1'")
        cursor.execute(get_substitutes)

        for idx, name in enumerate(cursor, 1):
            print(idx, "-", name)

        print("\n")

        try:
            choice = int(input())
            if choice < 0 or choice > idx:
                pass

        except ValueError:
            continue

        print("\n")

        connection.commit()
