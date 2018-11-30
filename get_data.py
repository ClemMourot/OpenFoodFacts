import requests
import json
from classes import *
import mysql.connector
from constants import *


def get_categories(categories_list):

    for c_id, page in enumerate(categories_names_url):
        url = "http://fr.openfoodfacts.org/categorie/{}.json" .format(page)
        request = requests.get(url)
        result = json.loads(request.text)
        category = Category()
        category.id = c_id
        category.name = categories_names_code[c_id]
        category.products_nb = result["count"]
        categories_list.append(category)


def get_products(products_list):

    for idx, page in enumerate(categories_names_url, 1):
        url = "http://fr.openfoodfacts.org/categorie/{}/{}.json" .format(page, idx)
        request = requests.get(url)
        result = json.loads(request.text)
        products = result["products"]
        for p_id, item in enumerate(products):
            if "generic_name" in item:
                product = Product()
                product.name = item["generic_name"]
                product.id = p_id
                product.category_id = idx
                products_list.append(product)


def add_categories(categories_list, cursor):

    for c_id, category in enumerate(categories_list):

        add_category = ("INSERT INTO categories "
                      "(name, products_number) "
                      "VALUES (%s, %s)")

        category_data = (categories_list[c_id].name, categories_list[c_id].products_nb)

        cursor.execute(add_category, category_data)


def add_products(products_list, cursor):

    for p_id, product in enumerate(products_list):

        add_product = ("INSERT INTO products "
                    "(name, category_id) "
                    "VALUES (%s, %s)")

        product_data = (products_list[p_id].name, products_list[p_id].category_id)

        cursor.execute(add_product, product_data)


def insert_into_database():

    categories_list = []
    products_list = []

    get_categories(categories_list)
    get_products(products_list)

    cnx = mysql.connector.connect(user='user', database='open_food_facts')
    cursor = cnx.cursor()

    add_categories(categories_list, cursor)
    add_products(products_list, cursor)

    cnx.commit()

    cursor.close()
    cnx.close()


insert_into_database()
