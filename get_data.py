import requests
import json
import mysql.connector

pages_nb = 10

url = "http://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux.json"
r = requests.get(url)
result = json.loads(r.text)
products_nb = result["count"]
print(products_nb)

for page in range(1, pages_nb):
    url = "http://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux/{0}.json" .format(page)
    print(url)
    r = requests.get(url)
    result = json.loads(r.text)
    print(r.text)
    product = result["products"]
    print(product)
    for i in product:
        if "generic_name" in i:
            print(i["generic_name"])


cnx = mysql.connector.connect(user='user', database='open_food_facts')
cursor = cnx.cursor()


