""" gets the data from the API and inserts it into the database if needed"""


def add_tables(connection, cursor):
    """sends sql requests to create the categories and products tables
    with all their columns"""

    drop_tables_p = "DROP TABLE IF EXISTS products "
    drop_tables_c = "DROP TABLE IF EXISTS categories "
    # makes sure the tables don't already exist

    cursor.execute(drop_tables_p)
    cursor.execute(drop_tables_c)
    connection.commit()

    add_categories_t = ("CREATE TABLE categories ("
                        "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,"
                        "name VARCHAR(50) NOT NULL,"
                        "products_number MEDIUMINT UNSIGNED NOT NULL,"
                        "PRIMARY KEY(id))"
                        "ENGINE=INNODB;")

    cursor.execute(add_categories_t)
    connection.commit()

    add_products_t = ("CREATE TABLE products ("
                      "p_id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,"
                      "name TEXT NOT NULL,"
                      "category_id SMALLINT UNSIGNED NOT NULL,"
                      "url TEXT NOT NULL,"
                      "score INT UNSIGNED NOT NULL,"
                      "saved TINYINT(1),"
                      "PRIMARY KEY(p_id),"
                      "CONSTRAINT fk_category_id FOREIGN KEY (category_id) "
                      "REFERENCES categories(id))"
                      "ENGINE=INNODB;")

    cursor.execute(add_products_t)
    connection.commit()


def add_categories(database, connection, cursor):
    """inserts categories data into database"""

    for c_id in enumerate(database.categories):
        #  browses the list to gather all the data stored in the objects

        add_category = ("INSERT INTO categories "
                        "(name, products_number) "
                        "VALUES (%s, %s)")

        category_data = (database.categories[c_id].name,
                         database.categories[c_id].products_nb)

        cursor.execute(add_category, category_data)
        connection.commit()


def add_products(database, connection, cursor):
    """inserts products data into database"""

    for p_id in enumerate(database.products):
        #  browses the list to gather all the data stored in the objects

        add_product = ("INSERT INTO products "
                       "(name, category_id, url, score) "
                       "VALUES (%s, %s, %s, %s)")

        product_data = (database.products[p_id].name,
                        str(database.products[p_id].category_id),
                        database.products[p_id].url,
                        str(database.products[p_id].score))

        cursor.execute(add_product, product_data)
        connection.commit()


def insert_into_database(database, connection, cursor):
    """calls every function needed to insert the data into the database"""

    check_tables = ("SHOW TABLES "
                    "LIKE 'products'")

    database.cursor.execute(check_tables)

    if not cursor.fetchone():  # if no result from the Xcursor
        print("Chargement des donnnées ...")
        database.get_categories()  # from the API
        database.get_products()
        add_tables(connection, cursor)

        add_categories(database, connection, cursor)  # into the MySQL database
        add_products(database, connection, cursor)
