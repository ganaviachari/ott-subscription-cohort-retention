# OTT Subscription Cohort & Retention Analysis

## Project overview
This beginner-friendly data analytics project explores an OTT/Netflix-style subscriber dataset using Python, SQL, and charts.

## Dataset
- Source file: `netflix_userbase_dataset.csv`
- Cleaned file: `cleaned_netflix_userbase.csv`
- Rows after cleaning: 3,000
- Columns: `user_id`, `subscription_start_date`, `subscription_plan`, `country`, plus derived cohort/date fields. Plans include Mobile, Basic, Standard, and Premium.

## Cleaning steps
1. Standardized column names and trimmed text values.
2. Converted subscription start dates to dates.
3. Removed rows missing required fields or with invalid plans.
4. Removed duplicate user IDs.
5. Added `cohort_month` and `subscription_start_year`.

## Charts
1. Monthly new subscriptions
2. Subscription plan distribution
3. Top 10 countries by subscribers
4. Plan mix across top 10 countries
5. Subscriber acquisition cohort size by month

Charts are saved in `charts/`.

## Tools
- Python: pandas, matplotlib
- SQL: MySQL 8+
- CSV dataset

## Run the Python analysis
Install requirements and run:

```bash
pip install -r requirements.txt
python analysis.py
```

## SQL
Open `sql_analysis.sql` in MySQL Workbench or your SQL editor. Import `cleaned_netflix_userbase.csv` into a table named `ott_subscriptions` first.

## Important note about retention
The provided dataset only contains user ID, subscription start date, plan, and country. It has no cancellation date, subscription status history, or monthly active-user data. So it can show **acquisition cohorts and subscriber mix**, but it cannot honestly calculate true monthly retention or churn. A commented SQL template is included for when monthly activity data becomes available.

## Upload to GitHub
1. Sign in to GitHub and create a new repository, for example `ott-subscription-cohort-retention`.
2. Extract this ZIP file on your computer.
3. Open the extracted folder in VS Code, or upload the files through GitHub's **Add file → Upload files**.
4. Commit the files with a message such as `Add OTT cohort analysis project`.
5. Do not upload passwords, API keys, or private data.

## Suggested GitHub description
OTT subscription cohort and subscriber analysis using Python, SQL, and data visualization. Includes data cleaning, acquisition cohort analysis, SQL queries, and five charts.
