"""
OTT Subscription Cohort & Retention Analysis
Run: python analysis.py
Input: cleaned_netflix_userbase.csv
Outputs: charts/*.png and analysis_summary.txt

Important limitation:
The source has user_id, subscription_start_date, subscription_plan, and country only.
It does not contain cancellation dates, monthly activity, or a subscription status history.
Therefore this project analyzes acquisition cohorts and subscriber mix; it cannot calculate
true retention/churn without additional monthly activity or cancellation data.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "cleaned_netflix_userbase.csv"
CHARTS = ROOT / "charts"
CHARTS.mkdir(exist_ok=True)

df = pd.read_csv(INPUT, parse_dates=["subscription_start_date"])
required = ["user_id", "subscription_start_date", "subscription_plan", "country"]
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

df = df.dropna(subset=required).drop_duplicates(subset=["user_id"])
df["cohort_month"] = df["subscription_start_date"].dt.to_period("M").astype(str)

monthly = df.groupby(df["subscription_start_date"].dt.to_period("M")).size()
fig, ax = plt.subplots(figsize=(10, 5))
monthly.plot(marker="o", ax=ax)
ax.set(title="Monthly New Subscriptions", xlabel="Month", ylabel="Users")
ax.tick_params(axis="x", rotation=60); fig.tight_layout()
fig.savefig(CHARTS / "01_monthly_subscriptions.png", dpi=160); plt.close(fig)

plans = df["subscription_plan"].value_counts()
fig, ax = plt.subplots(figsize=(8, 5))
plans.reindex(["Mobile", "Basic", "Standard", "Premium"]).dropna().plot(kind="bar", ax=ax)
ax.set(title="Subscription Plan Distribution", xlabel="Plan", ylabel="Users")
ax.tick_params(axis="x", rotation=0); fig.tight_layout()
fig.savefig(CHARTS / "02_plan_distribution.png", dpi=160); plt.close(fig)

countries = df["country"].value_counts().head(10).sort_values()
fig, ax = plt.subplots(figsize=(9, 6))
countries.plot(kind="barh", ax=ax)
ax.set(title="Top 10 Countries by Subscribers", xlabel="Users", ylabel="Country")
fig.tight_layout(); fig.savefig(CHARTS / "03_top_countries.png", dpi=160); plt.close(fig)

cross = pd.crosstab(df["country"], df["subscription_plan"])
top = df["country"].value_counts().head(10).index
cross = cross.loc[cross.index.intersection(top)]
cross = cross.reindex(columns=["Basic", "Standard", "Premium"], fill_value=0)
fig, ax = plt.subplots(figsize=(10, 6))
cross.plot(kind="barh", stacked=True, ax=ax)
ax.set(title="Plan Mix Across Top 10 Countries", xlabel="Users", ylabel="Country")
fig.tight_layout(); fig.savefig(CHARTS / "04_plan_by_country.png", dpi=160); plt.close(fig)

cohorts = df.groupby("cohort_month").size()
fig, ax = plt.subplots(figsize=(10, 5))
cohorts.plot(kind="bar", ax=ax)
ax.set(title="Subscriber Acquisition Cohort Size", xlabel="Cohort month", ylabel="New users")
ax.tick_params(axis="x", rotation=60); fig.tight_layout()
fig.savefig(CHARTS / "05_cohort_size.png", dpi=160); plt.close(fig)

summary = [
    f"Clean rows/users: {len(df)}",
    f"Date range: {df['subscription_start_date'].min().date()} to {df['subscription_start_date'].max().date()}",
    f"Countries: {df['country'].nunique()}",
    f"Plans: {df['subscription_plan'].nunique()}",
    "",
    "Plan counts:",
    df["subscription_plan"].value_counts().to_string(),
    "",
    "Top 10 countries:",
    df["country"].value_counts().head(10).to_string(),
    "",
    "Monthly new subscriptions:",
    df.groupby(df["subscription_start_date"].dt.to_period("M")).size().to_string(),
    "",
    "Retention limitation: no cancellation dates or monthly activity data were provided.",
]
(ROOT / "analysis_summary.txt").write_text("\n".join(summary), encoding="utf-8")
print("\n".join(summary))
