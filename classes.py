import requests
import json
from constants import *


class Product:

    def __init__(self):
        self.name = ""
        self.id = 0
        self.category_id = 0
        self.saved = 0
        self.score = 0
        self.url = ""


class Category:

    def __init__(self):
        self.name = ""
        self.id = 0
        self.products_nb = 0


class Database:

    def __init__(self):
        self.categories = []
        self.products = []
        self.substitutes = []

    def get_categories(self):

        for c_id, page in enumerate(categories_names_url):
            url = categories_welcome_page.format(page)
            print(url)
            request = requests.get(url)
            result = json.loads(request.text)
            category = Category()
            category.id = c_id
            category.name = categories_names_code[c_id]
            category.products_nb = result["count"]
            self.categories.append(category)

    def get_products(self):

        for idx, category in enumerate(categories_names_url, 1):

            for page in range(1, pages_nb_limit):

                url = products_page.format(category, page)
                request = requests.get(url)
                result = json.loads(request.text)
                products = result["products"]
                for p_id, item in enumerate(products):
                    if "generic_name_fr" in item and item["generic_name_fr"] != "" and "nutrition_grades" in item:
                        product = Product()
                        product.name = item["generic_name_fr"]
                        product.id = p_id
                        product.category_id = idx
                        product.url = item["url"]
                        score = item["nutrition_grades"]
                        product.score = scores.index(score) + 1
                        self.products.append(product)
