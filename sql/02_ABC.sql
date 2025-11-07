SELECT "Sub-Category",
	ROUND(SUM("Sales"), 1) AS Total_Sale,
	ROUND(
		SUM("Sales") * 100 / (
			SELECT SUM("Sales")
			FROM orders
		), 1
	) AS Percent
FROM orders
GROUP BY "Sub-Category"
ORDER BY Total_Sale DESC;