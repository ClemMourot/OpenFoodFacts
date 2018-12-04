import requests
import json
from classes import *
from constants import *


def get_categories(database):

    for c_id, page in enumerate(categories_names_url):
        url = "http://fr.openfoodfacts.org/categorie/{}.json" .format(page)
        request = requests.get(url)
        result = json.loads(request.text)
        category = Category()
        category.id = c_id
        category.name = categories_names_code[c_id]
        category.products_nb = result["count"]
        database.categories.append(category)


def get_products(database):

    for idx, category in enumerate(categories_names_url, 1):

        for page in range(1, pages_nb_limit):

            url = "http://fr.openfoodfacts.org/categorie/{}/{}.json" .format(category, page)
            request = requests.get(url)
            result = json.loads(request.text)
            products = result["products"]
            for p_id, item in enumerate(products):
                if "generic_name_fr" in item and item["generic_name_fr"] != "" and "nutrition_grades_tags" in item:
                    product = Product()
                    product.name = item["generic_name_fr"]
                    product.id = p_id
                    product.category_id = idx
                    product.url = item["url"]
                    product.score = item["nutrition_grades_tags"]
                    database.products.append(product)


def add_categories(database, connection, cursor):

    for c_id, category in enumerate(database.categories):

        add_category = ("INSERT INTO categories "
                      "(name, products_number) "
                      "VALUES (%s, %s)")

        category_data = (database.categories[c_id].name, database.categories[c_id].products_nb)

        cursor.execute(add_category, category_data)
        connection.commit()


def add_products(database, connection, cursor):

    for p_id, product in enumerate(database.products):

        add_product = ("INSERT INTO products "
                    "(name, category_id, url, score) "
                    "VALUES (%s, %s, %s, %s)")

        product_data = (database.products[p_id].name, database.products[p_id].category_id,
                        database.products[p_id].url, database.products[p_id].score)

        cursor.execute(add_product, product_data)
        connection.commit()


def insert_into_database(database, connection, cursor):

    get_categories(database)
    get_products(database)

    add_categories(database, connection, cursor)
    add_products(database, connection, cursor)

