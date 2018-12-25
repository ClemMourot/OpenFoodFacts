from constants import *


def categories_display(cursor):
    """displays categories and returns the user's choice"""

    user_input = False

    while not user_input:  # until the user chooses a category

        print("Trouver un substitut")
        print("\n")
        print("Sélectionnez la catégorie :")
        print("\n")

        get_categories = "SELECT name FROM categories"
        # sql request to get the categories names
        cursor.execute(get_categories)

        for idx, category in enumerate(cursor, 1):
            print(idx, "-", category)

        print("\n")

        try:

            choice = int(input())

            if choice <= 0 or choice > CATEGORIES_NB:
                # if user's choice is not valid

                print("Choix invalide")

            else:

                user_input = True
                return choice

        except ValueError:

            continue


def products_display(cursor, category_choice):
    """displays the products for the chosen category
    and returns the user's choice"""

    user_input = False

    while not user_input:  # until the user chooses a product

        print("\n")
        print("Sélectionnez l'aliment")

        get_products = ("SELECT name, p_id FROM products "
                        "WHERE category_id = %d ") % category_choice
        # sql request to get the products names and ids from the chosen category
        cursor.execute(get_products)

        idx = 0

        for idx, (name, p_id) in enumerate(cursor, 1):
            print(p_id, "-", name)
            idx = p_id

        print("\n")

        try:

            choice = int(input())

            if choice <= 0 or choice > idx:  # if user's choice is not valid

                print("Choix invalide")

            else:

                user_input = True
                return choice

        except ValueError:

            continue


def item_display(cursor, connection, product_choice):
    """displays the chosen product's details
    and call the get_substitute function if one can be found"""

    on = True

    while on:  # until the user chooses to return to the menu

        print("\n")
        print("Voici les détails de l'aliment choisi :")

        get_item = ("SELECT name, url, score, category_id FROM products "
                    "WHERE p_id = %d ") % product_choice
        # sql request to get the details on the chosen product
        cursor.execute(get_item)

        for idx, (name, url, score, category_id) in enumerate(cursor, 1):

            print("Nom du produit : ", name, "\n",
                  "Lien vers la page produit : ", url, "\n", "Nutriscore : ",
                  SCORES[score - 1])

            if score != 1:
                # a substitute can be found only
                # if the product's nutrition score isn't already the lowest

                on = get_substitute(cursor, connection, score, category_id,
                                    product_choice)
                # gets False when user wants to return to menu

            else:

                print("\n Ce produit n'a pas de substitut")
                print("Appuyez sur 'E' pour retourner au menu")

                key = input()

                if key == 'E':
                    on = False


def substitute_details(choice, cursor, connection):
    """displays the chosen substitute details and allow to unsave it"""

    print("Voici les détails du substitut choisi")

    get_selection = ("SELECT name, url, score, category_id FROM products "
                     "WHERE p_id = %d ") % choice
    cursor.execute(get_selection)

    for name, url, score, category_id in cursor:

        print("Nom du produit : ", name, "\n", "Lien vers la page produit : ",
              url, "\n", "Nutriscore : ",
              SCORES[score - 1], "\n", "Catégorie : ",
              CATEGORIES_NAMES_URL[category_id - 1])

        print(
            "Appuyez sur 'S' si vous voulez retirer ce produit "
            "de vos aliments substitués ou sur 'E' pour retourner au menu")

        key = input()

        if key == 'S':
            delete_substitute = ("UPDATE products SET saved = '0'"  
                                 "WHERE p_id = %d ") % choice
            # sql request to set back the saved column to '0'
            cursor.execute(delete_substitute)
            connection.commit()

        if key == 'E':
            return False


def substitutes_display(cursor, connection):
    """displays all the saved substitutes if any and calls
    the substitute_details function
    if the user chooses one to get more info on it"""

    on = True

    while on:  # until the user chooses to return to the menu

        print("Mes aliments substitués")

        get_substitutes = ("SELECT name, p_id FROM products "
                           "WHERE saved = '1'")
        cursor.execute(get_substitutes)

        idx = 0
        s_id = 0

        for idx, (name, s_id) in enumerate(cursor, 1):
            print(s_id, "-", name)

        if idx == 0:
            # if the cursor was empty
            # (meaning there was no product where the column saved equaled '1')

            print("Vous n'avez enregistré aucun substitut")
            print("Appuyez sur 'E' pour retourner au menu")

            key = input()

            if key == 'E':
                on = False

        else:  # if there are saved substitutes

            print("\n")

            print("Sélectionnez un substitut")

            try:

                choice = int(input())

                if choice <= 0 or choice > s_id:
                    # if user's choice is not valid

                    print("Choix invalide")

                else:

                    on = substitute_details(choice, cursor, connection)
                    # displays the substitute's details
                    # and returns False when user chooses to return to menu

            except ValueError:

                continue

            print("\n")

            connection.commit()


def get_substitute(cursor, connection, score, category_id, product_choice):
    """gets a substitute for the chosen product"""

    print("\n")
    print("Voici un substitut pour cet aliment :")

    substitute_request = ("SELECT name, url, score, saved, category_id, "
                          "p_id FROM products "
                          "WHERE score < %d AND p_id != %d"
                          " AND category_id = %d "
                          "ORDER BY RAND() LIMIT 1") % (
                             score, product_choice, category_id)
    #  sql request to select a random product from the same category
    #  and that has a lower nutrition score
    cursor.execute(substitute_request)

    idx = 0

    for idx, (name, url, score, saved, category_id, s_id) \
            in enumerate(cursor, 1):

        print("Nom du produit : ", name, "\n", "Lien vers la page produit : ",
              url, "\n", "Nutriscore : ",
              SCORES[int(score) - 1], "\n", "Catégorie : ",
              CATEGORIES_NAMES_URL[int(category_id) - 1])

        if saved == 1:  # if the substitute displayed has already been saved

            print("Vous avez déjà enregistré ce substitut")
            print("Appuyez sur 'E' pour retourner au menu")

            key = input()

            if key == 'E':
                return False

        elif saved != 1:

            print("\n")
            print(
                "Appuyez sur 'S' pour sauvegarder cet aliment "
                "ou sur 'E' pour retourner au menu")

            key = input()

            if key == 'S':
                save_substitute = ("UPDATE products SET saved = '1'"
                                   "WHERE p_id = %d ") % s_id
                # sql request to set the saved column to '1'
                cursor.execute(save_substitute)
                connection.commit()

            if key == 'E':
                return False

    if idx == 0:  # if the cursor was empty

        print("Ce produit n'a pas de substitut")


def replace_product(cursor, connection):
    """calls every function needed to get a substitute
    for a chosen product in a chosen category"""

    on = True

    while on:
        choice = categories_display(cursor)
        choice = products_display(cursor, choice)
        item_display(cursor, connection, choice)

        on = False
