import requests
import json
from classes import *
import mysql.connector
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
                if "generic_name_fr" in item and item["generic_name_fr"] != "":
                    product = Product()
                    product.name = item["generic_name_fr"]
                    product.id = p_id
                    product.category_id = idx
                    database.products.append(product)


def add_categories(database, cursor):

    for c_id, category in enumerate(database.categories):

        add_category = ("INSERT INTO categories "
                      "(name, products_number) "
                      "VALUES (%s, %s)")

        category_data = (database.categories[c_id].name, database.categories[c_id].products_nb)

        cursor.execute(add_category, category_data)


def add_products(database, cursor):

    for p_id, product in enumerate(database.products):

        add_product = ("INSERT INTO products "
                    "(name, category_id) "
                    "VALUES (%s, %s)")

        product_data = (database.products[p_id].name, database.products[p_id].category_id)

        cursor.execute(add_product, product_data)


def insert_into_database(database):

    get_categories(database)
    get_products(database)

    """cnx = mysql.connector.connect(user='user', database='open_food_facts')
    cursor = cnx.cursor()

    add_categories(database, cursor)
    add_products(database, cursor)

    cnx.commit()

    cursor.close()
    cnx.close()"""
