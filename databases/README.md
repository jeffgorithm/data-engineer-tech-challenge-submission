# ER Diagram
<p align="center">
    <img src="er-diagram.png" alt="er-diagram"/>
</p>

# Prerequisites
- Docker Engine
- Python 3
- Pip

# Technologies
- Docker
- PostgreSQL
- SQL Alchemy
- Psycopg

# Setup
1. Build custom PostgreSQL Docker image, pull official PostgreSQL image and add create_table.sql to create tables upon container start up
    ```
    sh scripts/build.sh
    ```
2. Create new Python virtual environment
    ```
    python -m venv venv
    ```
3. Activate Python virtual environment
    ```
    source venv/bin/activate
    ```
4. Install Python dependencies
    ```
    pip install -r requirements.txt
    ```

# Run
1. Start Docker container, new database and tables will be created upon start
    ```
    sh scripts/run.sh
    ```
2. Insert 50 rows of data into members table
    ```
    python insert_data.py
    ```
3. Verify rows are inserted by connecting via psql console
    ```
    # Connect to DB via psql command
    psql -h localhost -U postgres

    # Enter password=postgres when prompted

    # Execute the following SQL statement
    SELECT * FROM members;
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

# Handling Database at Scale

> TLDR: It is easier to scale read-heavy applications than write-heavy applications

## Write Heavy Application

### Short-term solutions
1. Use vertical scaling to allow for higher write performance/throughput

### Long-term solutions
1. Introduce queue component (i.e. Kafka, MQ, etc.) in front of database to insert records into database at a consistent rate

## Read Heavy Application

### Short-term solutions
1. Use vertical scaling to allow for higher read performance/throughput

### Long-term solutions
1. Horizontal scaling, use multiple read-replicas to handle high amount of reads
2. Cache data using a in-memory solution (e.g. Redis)
3. Perform partitioning or sharding of tables based on a key (requires domain knowledge to decide of partition/shard key)