class Product:

    def __init__(self):
        self.name = ""
        self.id = 0
        self.category_id = 0


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
