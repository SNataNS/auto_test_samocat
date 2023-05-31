SELECT c.login, COUNT(o.id) AS "countOrders" 
FROM "Couriers" AS c
WHERE o."inDelivery"=true 
INNER JOIN "Orders" AS o
ON c.id =o."courierId"
GROUP BY c.login;
