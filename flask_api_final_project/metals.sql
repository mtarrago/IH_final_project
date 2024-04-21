/*
This dataset consists of 2 files:

Mining Production by Major States and Municipalities: Contains indicators related to the 
products and volume of minerometallurgical production by federal entities and municipalities, 
where mining activity exists.

Minerometallurgical Production by Main Products: Contains indicators related to the products, volume, 
and value of national minerometallurgical production.
*/
-- 1. define potential resources
-- locations
-- products

-- 2. potential endpoints
-- /products
-- /products/<product_name>
-- /products/<product_group> 
-- /locations
-- /locations/state
-- /locations/state/municipality

-- 3. structure
-- /products/<product_name> (initial focus)
	-- product group
	-- volume
	-- volume units
    -- value
	-- locations (states)
    -- locations (municipality)
	-- year
    -- report status
-- products (with pagination)
-- location by state
	-- products
	-- aggregated volume
    -- volume units
    -- aggregated value
-- location by municipality
	-- products
	-- aggregated volume
    -- volume units
    -- aggregated value
    


select * from products;


select * from locations;

select distinct product from products 
where product_group like "Precious Metals";

select distinct product_group from products;

SELECT P.PRODUCT AS product
,P.PRODUCT_GROUP AS product_group
,P.VOLUME AS volume
,P.MEASUREMENT_UNIT AS units
,P.VALUE AS value
,P.YEAR AS year
,L.STATE AS state           
            FROM PRODUCTS P   
            JOIN locations L ON P.PRODUCT = L.PRODUCT;
            
select distinct p.product, l.state from products p
join locations l
on p.product = l.product
where p.product like "Barite" and p.YEAR like "2023";

select p.product, round(sum(p.volume)) as total_volume, p.MEASUREMENT_UNIT from products p
                            join locations l
	                            on p.product = l.product
                            WHERE P.product like "Gold"
                            group by  p.product, p.YEAR, p.MEASUREMENT_UNIT;

SELECT * FROM PRODUCTS
ORDER BY PRODUCT;
