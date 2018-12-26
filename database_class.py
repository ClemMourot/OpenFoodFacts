""" initializes database class"""

import json
import requests
import mysql.connector

from category_class import *
from product_class import*
from constants import *


class Database:
    """defines an object symmetrical to the MySQL database"""

    def __init__(self):
        """initializes lists containing all products and categories"""

        self.categories = []
        self.products = []
        self.connection = mysql.connector.connect(user='user',
                                                  database='open_food_facts')
        self.cursor = self.connection.cursor()  # connects to MySQL

    def get_categories(self):
        """gathers categories data via the API
        and instantiates a Category object with its attributes
        for every category, then adds it to the list"""

        for c_id, page in enumerate(CATEGORIES_NAMES_URL):
            # browses the list of selected categories

            url = CATEGORIES_WELCOME_PAGE.format(page)
            request = requests.get(url)
            result = json.loads(request.text)
            # turns json result into a dictionary
            category = Category()
            category.c_id = c_id
            category.name = CATEGORIES_NAMES_URL[c_id]
            category.products_nb = result["count"]
            self.categories.append(category)

    def get_products(self):
        """gathers products data via the API and instantiates a Product object
        with its attributes for every product, then adds it to the list"""

        for idx, category in enumerate(CATEGORIES_NAMES_URL, 1):
            # browses the list of selected categories

            for page in range(1, LIMIT_PAGES_NB):
                # browses the pages within the defined limit

                url = PRODUCTS_PAGE.format(category, page)
                request = requests.get(url)
                result = json.loads(request.text)
                products = result["products"]

                for p_id, item in enumerate(products):
                    # browses the dictionary of products

                    if "generic_name_fr" in item \
                            and item["generic_name_fr"] != "" \
                            and "nutrition_grades" in item:
                        # makes sure we don't get a product
                        # that doesn't have a name or a nutrition grade

                        product = Product()
                        product.name = item["generic_name_fr"]
                        product.p_id = p_id
                        product.category_id = idx
                        product.url = item["url"]
                        score = item["nutrition_grades"]
                        product.score = SCORES.index(score) + 1
                        # translates the letter score into a numeric one
                        self.products.append(product)
