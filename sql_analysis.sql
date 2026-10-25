-- OTT Subscription Cohort & Retention Analysis (MySQL 8+)
-- Import cleaned_netflix_userbase.csv into a table named ott_subscriptions.
-- Suggested columns:
-- user_id VARCHAR(30) PRIMARY KEY,
-- subscription_start_date DATE,
-- subscription_plan VARCHAR(20),
-- country VARCHAR(100),
-- cohort_month CHAR(7)

-- 1. Validate row count and duplicates
SELECT COUNT(*) AS total_users FROM ott_subscriptions;
SELECT user_id, COUNT(*) AS duplicate_count
FROM ott_subscriptions GROUP BY user_id HAVING COUNT(*) > 1;

-- 2. Monthly new subscriptions
SELECT DATE_FORMAT(subscription_start_date, '%Y-%m') AS signup_month,
       COUNT(*) AS new_subscriptions
FROM ott_subscriptions
GROUP BY signup_month
ORDER BY signup_month;

-- 3. Plan distribution
SELECT subscription_plan, COUNT(*) AS users,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM ott_subscriptions), 2) AS pct_users
FROM ott_subscriptions
GROUP BY subscription_plan
ORDER BY users DESC;

-- 4. Top 10 countries
SELECT country, COUNT(*) AS users
FROM ott_subscriptions
GROUP BY country
ORDER BY users DESC
LIMIT 10;

-- 5. Plan mix by country
SELECT country,
       SUM(subscription_plan = 'Mobile') AS mobile_users,
       SUM(subscription_plan = 'Basic') AS basic_users,
       SUM(subscription_plan = 'Standard') AS standard_users,
       SUM(subscription_plan = 'Premium') AS premium_users,
       COUNT(*) AS total_users
FROM ott_subscriptions
GROUP BY country
ORDER BY total_users DESC;

-- 6. Acquisition cohort sizes
SELECT DATE_FORMAT(subscription_start_date, '%Y-%m') AS cohort_month,
       COUNT(*) AS cohort_size
FROM ott_subscriptions
GROUP BY cohort_month
ORDER BY cohort_month;

-- 7. Retention query TEMPLATE (requires a separate monthly activity table)
-- Create/populate ott_user_activity(user_id, activity_month), one row per active user/month.
-- Do not run this query until you have actual activity records.
--
-- WITH cohort AS (
--   SELECT user_id, DATE_FORMAT(subscription_start_date, '%Y-%m-01') AS cohort_month
--   FROM ott_subscriptions
-- ),
-- activity AS (
--   SELECT DISTINCT user_id, STR_TO_DATE(CONCAT(activity_month, '-01'), '%Y-%m-%d') AS activity_month
--   FROM ott_user_activity
-- ),
-- cohort_activity AS (
--   SELECT c.cohort_month, a.activity_month,
--          TIMESTAMPDIFF(MONTH, STR_TO_DATE(c.cohort_month, '%Y-%m-%d'), a.activity_month) AS month_number,
--          COUNT(DISTINCT c.user_id) AS active_users
--   FROM cohort c
--   JOIN activity a ON a.user_id = c.user_id
--   WHERE a.activity_month >= STR_TO_DATE(c.cohort_month, '%Y-%m-%d')
--   GROUP BY c.cohort_month, a.activity_month
-- )
-- SELECT cohort_month, month_number, active_users,
--        FIRST_VALUE(active_users) OVER (PARTITION BY cohort_month ORDER BY month_number) AS cohort_size,
--        ROUND(100.0 * active_users /
--          FIRST_VALUE(active_users) OVER (PARTITION BY cohort_month ORDER BY month_number), 2) AS retention_pct
-- FROM cohort_activity
-- ORDER BY cohort_month, month_number;
--
-- Important: subscription start dates alone cannot measure true retention or churn.
