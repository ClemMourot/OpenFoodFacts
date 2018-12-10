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

        product_data = (database.products[p_id].name, str(database.products[p_id].category_id),
                        database.products[p_id].url, str(database.products[p_id].score))

        cursor.execute(add_product, product_data)
        connection.commit()


def insert_into_database(database, connection, cursor):

    database.get_categories()
    database.get_products()

    add_categories(database, connection, cursor)
    add_products(database, connection, cursor)
