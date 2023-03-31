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