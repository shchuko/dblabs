-- ****************************************** --
-- ***** FILL TABLE WITH CSV FILES HERE ***** --
-- ****************************************** --

-- Update user's favourite address
UPDATE "GINZA"."User"
SET ("favourite_address") = (
    SELECT "GINZA"."UserAddress"."id"
    FROM "GINZA"."UserAddress"
    WHERE "user_id" = "GINZA"."User"."id"
);


-- Update order's price
UPDATE "GINZA"."Order"
SET ("total_price") = (
    SELECT COALESCE(SUM("price"), 0)
    FROM "GINZA"."OrderEntry"
    WHERE "GINZA"."OrderEntry"."order_id" = "GINZA"."Order"."id"
);
