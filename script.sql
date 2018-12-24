CREATE DATABASE open_food_facts;
USE open_food_facts;
CREATE USER 'user'@'localhost';
GRANT ALL PRIVILEGES ON open_food_facts.* TO 'user'@'localhost';
exit;