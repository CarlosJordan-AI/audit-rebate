-- Report: Audit counts and rebate within a date window
-- Params:
--   :start  (YYYY-MM-DD or ISO datetime)
--   :end    (YYYY-MM-DD or ISO datetime)
--   :partner (e.g., 'teepublicvip')
-- Notes:
-- - iscancelled/IsCancelled fields are 0/1 integers
-- - od.ismugprint/isstickerprint are 0/1 integers
-- - o.type 'reprint' is excluded

SELECT
  COUNT(DISTINCT o.id)                         AS numOrdersRecv,
  COUNT(odu.id)                                AS numUnitsRecv,
  COUNT(odu.id) * 0.25                         AS TotalRebate
FROM "order" o
JOIN orderdetail od       ON od.orderid = o.id
JOIN orderdetailunit odu  ON odu.orderdetailid = od.id
WHERE
  o.createdonutc >= :start
  AND o.createdonutc  < :end
  AND o.iscancelled = 0
  AND od.IsCancelled = 0
  AND odu.iscancelled = 0
  AND od.ismugprint = 0
  AND od.isstickerprint = 0
  AND o.type <> 'reprint'
  AND o.CustomPartnerId = :partner;
