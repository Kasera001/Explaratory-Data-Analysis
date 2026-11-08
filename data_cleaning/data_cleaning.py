import numpy as np  # type: ignore[import-not-found]
import pandas as pd  # type: ignore[import-not-found]
import random
from pathlib import Path

rng = np.random.default_rng(42)
random.seed(42)

N = 5000

catalog = {
    "Dairy":     [("Fresh Milk 500ml", 60), ("Yoghurt 250ml", 85), ("Butter 250g", 320)],
    "Grains":    [("Maize Flour 2kg", 190), ("Rice 1kg", 180), ("Wheat Flour 2kg", 210)],
    "Beverages": [("Tea Leaves 250g", 120), ("Soda 500ml", 70), ("Juice 1L", 190)],
    "Household": [("Detergent 1kg", 260), ("Bar Soap", 50), ("Toilet Paper 10pk", 350)],
    "Produce":   [("Tomatoes 1kg", 120), ("Onions 1kg", 110), ("Sukuma Wiki Bunch", 30)],
}
branches = ["Nakuru", "Nairobi", "Mombasa", "Kisumu", "Eldoret"]
branch_w = [0.30, 0.30, 0.15, 0.10, 0.15]

# ---------- 1. Generate CLEAN data ----------
days = pd.date_range("2025-01-01", "2025-12-31")
day_w = np.where(days.month == 12, 1.6, 1.0)      # December is busier
day_w = day_w / day_w.sum()
dates = rng.choice(days, N, p=day_w)

categories = rng.choice(list(catalog), N)
product_names, base_prices = [], []
for c in categories:
    name, price = catalog[c][rng.integers(0, 3)]
    product_names.append(name)
    base_prices.append(price)

df = pd.DataFrame({
    "transaction_id": [f"T{100000 + i}" for i in range(N)],
    "date": pd.to_datetime(dates),
    "branch": rng.choice(branches, N, p=branch_w),
    "customer_id": ["C" + str(x).zfill(4) for x in rng.integers(1, 1501, N)],
    "customer_age": np.clip(rng.normal(34, 11, N), 18, 70).round(),
    "gender": rng.choice(["Male", "Female"], N),
    "product_category": categories,
    "product_name": product_names,
    "quantity": rng.integers(1, 11, N),
    "unit_price_kes": (np.array(base_prices) * rng.uniform(0.95, 1.08, N)).round(0),
    "discount_pct": rng.choice([0, 0, 0, 5, 10, 15], N),
    "payment_method": rng.choice(["M-Pesa", "Cash", "Card"], N, p=[0.6, 0.3, 0.1]),
    "customer_rating": rng.integers(1, 6, N).astype(float),
})
df["total_kes"] = (df["quantity"] * df["unit_price_kes"] * (1 - df["discount_pct"] / 100)).round(2)

# ---------- 2. Make it DIRTY ----------
def pick(frac):
    return rng.choice(df.index, size=int(frac * len(df)), replace=False)

# Duplicates (3%), then shuffle
dups = df.sample(frac=0.03, random_state=1)
df = pd.concat([df, dups]).sample(frac=1, random_state=2).reset_index(drop=True)

# Missing values
df.loc[pick(0.08), "customer_age"] = np.nan
df.loc[pick(0.15), "customer_rating"] = np.nan
df.loc[pick(0.04), "payment_method"] = np.nan
df.loc[pick(0.05), "gender"] = np.nan

# Inconsistent gender labels
idx = pick(0.20)
df.loc[idx, "gender"] = df.loc[idx, "gender"].map(
    {"Male": "M", "Female": "F"}).fillna(df.loc[idx, "gender"])
df.loc[pick(0.05), "gender"] = "male"

# Branch: casing, whitespace, typos
idx = pick(0.12)
df.loc[idx, "branch"] = df.loc[idx, "branch"].apply(
    lambda s: random.choice([s.upper(), s.lower(), " " + s + " ", s[:-1]]))

# Category typos / casing
mask = (df["product_category"] == "Dairy") & (rng.random(len(df)) < 0.2)
df.loc[mask, "product_category"] = "Diary"
df.loc[pick(0.03), "product_category"] = "grains"

# Mixed date formats + a few invalid dates
df["date"] = df["date"].dt.strftime("%Y-%m-%d")
idx = pick(0.30)
df.loc[idx, "date"] = pd.to_datetime(df.loc[idx, "date"]).dt.strftime("%d/%m/%Y")
df.loc[pick(0.005), "date"] = "unknown"

# Price stored as text in some rows
df["unit_price_kes"] = df["unit_price_kes"].astype(object)
idx = pick(0.05)
df.loc[idx, "unit_price_kes"] = df.loc[idx, "unit_price_kes"].apply(
    lambda p: f"KES {int(p):,}")

# Outliers and impossible values
df["customer_age"] = df["customer_age"].astype(float)
df.loc[pick(0.005), "customer_age"] = 200
df.loc[pick(0.003), "customer_age"] = -5
df.loc[pick(0.004), "quantity"] = -3
df.loc[pick(0.003), "quantity"] = 500
df.loc[pick(0.003), "discount_pct"] = 150

# ---------- 3. Save ----------
df.to_csv("savanna_retail_sales_raw.csv", index=False)
print(df.shape)
print(df.head())




#------4.DATA CLEAN  PROCESS--------#
csv_path = Path(__file__).with_name("savanna_retail_sales_raw.csv")
df = pd.read_csv(csv_path)

# shape and a first look
print(df.shape)
print(df.head())

#type and non-null counts
df.info()

# find the missing values
print(df.isna().sum())

# find duplicates
print(df.duplicated().sum())

# Numeric columns
print(df.describe())


# categorical columns
for col in ["branch","gender","product_category","payment_method"]:
    print(df[col].value_counts(dropna=False))
    print()   