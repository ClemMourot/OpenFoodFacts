	Use the data from Open Food Facts


REQUIREMENTS

- Python
- MySQL
- Internet connection


USER GUIDE

The user can choose between (1) finding a substitute for a food item or (2) accessing the already replaced food items.
If he chooses (1):
- he has to select one category
- he has to select one food item
- he can see the substitute for this food item
- he can save the result
If he chooses (2):
- he can see the list of his saved items
- he can choose one to see all the details
- he can remove one from the list


SOURCES

https://openclassrooms.com/fr/
https://dev.mysql.com/doc/connector-python/en
http://docs.python-requests.org
http://dridk.me/python-requests.html
https://en.wiki.openfoodfacts.org/API
https://stackoverflow.com
https://zestedesavoir.com
https://pynative.com/
https://www.wikipedia.org

SCRIPT MYSQL

CREATE DATABASE open_food_facts;
USE open_food_facts;
CREATE USER 'user'@'localhost';
GRANT ALL PRIVILEGES ON open_food_facts.* TO 'user'@'localhost';
exit;

