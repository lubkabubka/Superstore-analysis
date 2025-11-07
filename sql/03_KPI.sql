WITH temp AS (
	SELECT "Order ID",
		SUM("Profit") AS Order_Profit,
		MAX(
			CASE
				WHEN "Discount" > 0 THEN 1
				ELSE 0
			END
		) AS has_discount
	FROM orders
	WHERE "Order Date" BETWEEN :date_from AND :date_to
	-- CAT_FILTER
	GROUP BY "Order ID"
),
tot AS(
	SELECT COUNT("Order ID") as tot
	FROM temp
),
tot_los AS (
	SELECT COUNT("Order ID") as tot_los
	FROM temp
	WHERE "Order_Profit" < 0
),
tot_disc as (
    SELECT COUNT("Order ID") as dis
	FROM temp
	WHERE has_discount = 1
),
tot_disc_los as (
    SELECT COUNT("Order ID") as dis_los
	FROM temp
	WHERE "Order_Profit" < 0
	AND has_discount = 1
)
SELECT tot.tot,
	tot_los.tot_los,
	ROUND(100.0 * tot_los.tot_los / NULLIF(tot.tot, 0), 2) AS loss_rate_pct,
	tot_disc.dis,
	tot_disc_los.dis_los,
	ROUND(100.0 * tot_disc_los.dis_los / NULLIF(tot_disc.dis, 0), 2) AS dis_loss_rate_pct
FROM tot
    CROSS JOIN tot_los
    CROSS JOIN tot_disc
    CROSS JOIN tot_disc_los;