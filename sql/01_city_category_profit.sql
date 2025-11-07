select "City", "Category",
  ROUND(SUM("Profit"), 1) AS Total_Profit
FROM orders
GROUP BY "Region", "Category"
ORDER BY "Region", "Category";