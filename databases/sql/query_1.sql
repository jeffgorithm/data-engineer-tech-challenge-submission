SELECT a.membership_id, a.first_name, a.last_name, SUM(b.total_price) AS total
FROM members a
JOIN transactions t ON a.membership_id = b.membership_id
GROUP BY a.membership_id
ORDER BY total DESC
LIMIT 10;