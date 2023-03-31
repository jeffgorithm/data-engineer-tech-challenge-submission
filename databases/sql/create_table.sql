CREATE DATABASE ecommerce;

--Create Tables
CREATE TABLE members(
    membership_id VARCHAR PRIMARY KEY NOT NULL,
    first_name TEXT NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    date_of_birth VARCHAR NOT NULL,
    mobile_no VARCHAR NOT NULL,
    above_18 BOOLEAN
);

CREATE TABLE items(
    item_id INT PRIMARY KEY NOT NULL,
    item_name VARCHAR NOT NULL,
    manufacturer_name VARCHAR NOT NULL,
    cost FLOAT NOT NULL,
    weight FLOAT NOT NULL
);

CREATE TABLE transactions(
    transaction_id INT PRIMARY KEY NOT NULL,
    membership_id VARCHAR NOT NULL,
    total_items_price FLOAT NOT NULL,
    total_items_weight FLOAT NOT NULL,
    FOREIGN KEY (membership_id) REFERENCES members (membership_id)
);

CREATE TABLE transaction_details(
    id INT PRIMARY KEY NOT NULL,
    transaction_id INT NOT NULL,
    item_id INT NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions (transaction_id),
    FOREIGN KEY (item_id) REFERENCES items (item_id)
);