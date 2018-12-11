from classes import *
import get_data
import database_access
import mysql.connector
import sqlalchemy


def menu():

    print("\n")
    print("    MENU    ")
    print("\n")
    print("1 - Remplacer un aliment")
    print("2 - Retrouver mes aliments substitués")
    print("3 - Quitter")
    print("\n")

    choice = int(input())

    return choice


def program():

    database = Database()
    connection = mysql.connector.connect(user='user', database='open_food_facts')
    cursor = connection.cursor()
    # get_data.insert_into_database(database, connection, cursor)

    on = True
    while on:

        try:
            choice = menu()
            if choice <= 0 or choice > 3:
                pass

        except ValueError:
            continue

        if choice == 1:
            print("\n")
            database_access.replace_product(cursor, connection)

        if choice == 2:
            print("\n")
            database_access.substitutes_display(cursor, connection)

        if choice == 3:
            on = False

    cursor.close()
    connection.close()


program()


"""import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy.ext.declarative import declarative_base


def orm():
    engine = sqlalchemy.create_engine("mysql://user@localhost/open_food_facts",
                                      encoding='utf-8', echo=True)
    Base = declarative_base()

    class Cat(Base):

        __tablename__ = 'categories'

        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    cat = Cat(id='1')
    print(cat.id)


orm()"""
