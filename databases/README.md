# ER Diagram
<p align="center">
    <img src="er-diagram.png" alt="er-diagram"/>
</p>

# Prerequisites
- Docker Engine

# Technologies
- Docker
- PostgreSQL

# Setup
1. Build custom PostgreSQL Docker image, pull official PostgreSQL image and add create_table.sql to create tables upon container start up
    ```
    sh scripts/build.sh
    ```

# Run
1. Start Docker container, new database and tables will be created upon start
    ```
    sh scripts/run.sh
    ```

# SQL Queries
1. Which are the top 10 members by spending?
    ```
    SELECT a.membership_id, a.first_name, a.last_name, SUM(b.total_price) AS total
    FROM members a
    JOIN transactions t ON a.membership_id = b.membership_id
    GROUP BY a.membership_id
    ORDER BY total DESC
    LIMIT 10;
    ```
2. Which are the top 3 items that are frequently brought by members
    ```
    SELECT a.item_name, (COUNT(b.transaction_id) * b.quantity) AS total
    FROM items a
    JOIN transaction_details b ON a.transaction_id = b.transaction_id
    JOIN transactions c ON b.item_id = c.item_id
    GROUP BY a.item_id, a.item_name, c.quantity
    ORDER BY total DESC
    LIMIT 3;
    ```