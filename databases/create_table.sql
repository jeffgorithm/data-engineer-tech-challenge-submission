CREATE DATABASE ecommerce;

--Create Tables
CREATE TABLE members(
    id INT PRIMARY KEY NOT NULL,
    first_name TEXT NOT NULL,
    last_name varchar(36) NOT NULL,
    date_of_birth varchar(36) NOT NULL,
    email varchar(36) NOT NULL,
    mobile_no varchar(36) NOT NULL
);

CREATE TABLE items(
    id INT PRIMARY KEY NOT NULL,
    item_name varchar(36) NOT NULL,
    manufacturer_name varchar(36) NOT NULL,
    cost varchar(36) NOT NULL,
    weight varchar(36) NOT NULL
);

CREATE TABLE transactions(
    id INT PRIMARY KEY NOT NULL,
    membership_id INT NOT NULL,
    total_items_price INT NOT NULL,
    total_items_weight INT NOT NULL,
    FOREIGN KEY (membership_id) REFERENCES members (id)
);

CREATE TABLE transaction_details(
    id INT PRIMARY KEY NOT NULL,
    transaction_id INT NOT NULL,
    item_id INT NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions (id),
    FOREIGN KEY (item_id) REFERENCES items (id)
);