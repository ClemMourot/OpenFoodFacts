import requests
import json
from classes import *
import mysql.connector
from constants import *


def get_categories():

    categories_list = []

    for c_id, page in enumerate(categories_names_url):
        url = "http://fr.openfoodfacts.org/categorie/{}.json" .format(page)
        request = requests.get(url)
        result = json.loads(request.text)
        category = Category()
        category.id = c_id
        category.name = categories_names_code[c_id]
        category.products_nb = result["count"]
        categories_list.append(category)

        get_products()


def get_products():

    products_list = []

    for idx, page in enumerate(categories_names_url, 1):
        url = "http://fr.openfoodfacts.org/categorie/{}/{}.json" .format(page, idx)
        request = requests.get(url)
        result = json.loads(request.text)
        products = result["products"]
        for p_id, item in enumerate(products):
            if "generic_name_fr" in item:
                product = Product()
                product.name = p_id["generic_name_fr"]
                product.id = p_id
                products_list.append(product)


"""cnx = mysql.connector.connect(user='user', database='open_food_facts')
cursor = cnx.cursor()

TABLES = {}

TABLES['categories'] = (
    "CREATE TABLE categories"
)

TABLES['products'] = (
    "CREATE TABLE products"
)

"""

get_categories()

get_products()
