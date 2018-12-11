from constants import *


def categories_display(cursor):

    user_input = False

    while not user_input:

        print("Trouver un substitut")
        print("\n")
        print("Sélectionnez la catégorie :")
        print("\n")

        get_categories = "SELECT name FROM categories"
        cursor.execute(get_categories)

        for idx, category in enumerate(cursor, 1):
            print(idx, "-", category)

        print("\n")

        try:
            choice = int(input())
            if choice <= 0 or choice > categories_nb:
                print("Choix invalide")
            else:
                return choice
                user_input = True
        except ValueError:
            continue


def products_display(cursor, category_choice):

    user_input = False

    while not user_input:

        print("\n")
        print("Sélectionnez l'aliment")

        get_products = ("SELECT name, id FROM products "
                        "WHERE category_id = %d ") % category_choice
        cursor.execute(get_products)

        for idx, (name, id) in enumerate(cursor, 1):
            print(id, "-", name)

        print("\n")

        try:
            choice = int(input())
            if choice <= 0 or choice > id:
                print("Choix invalide")
            else:
                return choice
                user_input = True
        except ValueError:
            continue


def get_substitute(cursor, connection, score, category_id, product_choice):

    print("\n")
    print("Voici un substitut pour cet aliment :")

    substitute_request = ("SELECT name, url, score, id, saved FROM products "
                          "WHERE score < %d AND id != %d AND category_id = %d ORDER BY RAND() LIMIT 1") % (
                     score, product_choice, category_id)
    cursor.execute(substitute_request)

    for name, url, score, id, saved in cursor:
        print(name, url, score, id)

        if saved == 1:
            print("Vous avez déjà enregistré ce substitut")
            print("Appuyez sur 'E' pour retourner au menu")
            key = input()
            if key == 'E':
                return False

        elif saved != 1:
            print("\n")
            print("Appuyez sur 'S' pour sauvegarder cet aliment")

            key = input()
            if key == 'S':
                print("a")
                save_substitute = ("UPDATE products SET saved = '1'"
                                   "WHERE id = %d ") % id
                cursor.execute(save_substitute)
                connection.commit()
            if key == 'E':
                return False


def item_display(cursor, connection, product_choice):

    on = True
    while on:

        print("\n")
        print("Voici les détails de l'aliment choisi :")

        get_item = ("SELECT name, url, score, category_id FROM products "
                    "WHERE id = %d ") % product_choice
        cursor.execute(get_item)

        for idx, (name, url, score, category_id) in enumerate(cursor, 1):
            letter_score = scores[score-1]
            print("Nom du produit : ", name, "\n", "Lien vers la page produit : ", url, "\n", "Nutriscore : ", letter_score)
            if score != 1:
                on = get_substitute(cursor, connection, score, category_id, product_choice)
            else:
                print("\n Ce produit n'a pas de substitut")
                print("Appuyez sur 'E' pour retourner au menu")
                key = input()
                if key == 'E':
                    on = False


def replace_product(cursor, connection):

    on = True

    while on:

        choice = categories_display(cursor)
        choice = products_display(cursor, choice)
        item_display(cursor, connection, choice)

        on = False


def substitute_details(choice, cursor, connection):

    print("Voici les détails de l'aliment choisi")
    get_selection = ("SELECT name, url, score, category_id FROM products "
                     "WHERE id = %d ") % choice
    cursor.execute(get_selection)

    for name, url, score, category_id in cursor:
        print("Nom du produit : ", name, "\n", "Lien vers la page produit : ", url, "\n", "Nutriscore : ",
              scores[score - 1], "\n", "Catégorie : ", categories_names_code[category_id-1])
        print("Appuyez sur 'S' si vous voulez retirer ce produit de vos aliments substitués "
              "ou sur 'E' pour retourner au menu")
        key = input()
        if key == 'S':
            unsave_substitute = ("UPDATE products SET saved = '0'"
                                 "WHERE id = %d ") % choice
            cursor.execute(unsave_substitute)
            connection.commit()
        if key == 'E':
            return False


def substitutes_display(cursor, connection):

    on = True

    while on:

        print("Mes aliments substitués")

        get_substitutes = ("SELECT name, id FROM products "
                           "WHERE saved = '1'")
        cursor.execute(get_substitutes)

        idx = 1

        for idx, (name, id) in enumerate(cursor):
            print(id, "-", name)

        if idx is None:
            print("Vous n'avez enregistré aucun substitut")
            print("Appuyez sur 'E' pour retourner au menu")
            key = input()
            if key == 'E':
                on = False

        else:

                print("\n")

                print("Sélectionnez un substitut")

                try:
                    choice = int(input())
                    if choice <= 0 or choice > id:
                        print("Choix invalide")
                    else:
                        on = substitute_details(choice, cursor, connection)

                except ValueError:
                    continue

                print("\n")

                connection.commit()
