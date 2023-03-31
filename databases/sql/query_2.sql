SELECT a.item_name, (COUNT(b.transaction_id) * b.quantity) AS total
FROM items a
JOIN transaction_details b ON a.transaction_id = b.transaction_id
JOIN transactions c ON b.item_id = c.item_id
GROUP BY a.item_id, a.item_name, c.quantity
ORDER BY total DESC
LIMIT 3;