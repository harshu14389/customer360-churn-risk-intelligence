-- Illustrative SQL; adapt date and identifier syntax to the target engine.
-- Run against a table imported from synthetic_customer_snapshots.csv.
SELECT COUNT(*) AS row_count, COUNT(DISTINCT customer_id) AS customers
FROM CUSTOMER_SNAPSHOTS;
SELECT customer_id, COUNT(*) AS duplicate_count
FROM CUSTOMER_SNAPSHOTS GROUP BY customer_id HAVING COUNT(*) > 1;
SELECT COUNT(*) AS invalid_rows FROM CUSTOMER_SNAPSHOTS
WHERE signup_date > snapshot_date OR unresolved_tickets > tickets_last_90d
   OR activity_last_30d < 0 OR spend_last_90d < 0;
-- Matured outcome data is for retrospective evaluation, never a prediction feature.
SELECT snapshot_date, segment, COUNT(*) AS customers,
       AVG(CAST(churn_next_90d AS DECIMAL(10,4))) AS observed_churn_rate
FROM CUSTOMER_SNAPSHOTS GROUP BY snapshot_date, segment;
