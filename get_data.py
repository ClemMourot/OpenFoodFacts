def add_tables(connection, cursor):

    drop_tables = ("DROP TABLE IF EXISTS products;"
                   "DROP TABLE IF EXISTS categories;")

    cursor.execute(drop_tables, multi=True)
    connection.commit()

    add_categories_t = ("CREATE TABLE categories ("
                        "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,"
                        "name VARCHAR(30) NOT NULL,"
                        "products_number MEDIUMINT UNSIGNED NOT NULL,"
                        "PRIMARY KEY(id))"
                        "ENGINE=INNODB;")

    cursor.execute(add_categories_t)
    connection.commit()

    add_products_t = ("CREATE TABLE products ("
                      "id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,"
                      "name TEXT NOT NULL,"
                      "category_id SMALLINT UNSIGNED NOT NULL,"
                      "url TEXT NOT NULL,"
                      "score INT UNSIGNED NOT NULL,"
                      "saved TINYINT(1),"
                      "PRIMARY KEY(id),"
                      "CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES categories(id))"
                      "ENGINE=INNODB;")

    cursor.execute(add_products_t)
    connection.commit()


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

    add_tables(connection, cursor)

    add_categories(database, connection, cursor)
    add_products(database, connection, cursor)
