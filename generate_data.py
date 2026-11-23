import numpy as np
import pandas as pd

# Generator 1: Duka Electronics
rng1 = np.random.default_rng(2026)
n1 = 1000
products = {
    "Phone": 15000,
    "Laptop": 65000,
    "Headphones": 2500,
    "Tablet": 28000,
    "Charger": 1200,
}

sales = pd.DataFrame({
    "order_id": range(1001, 1001 + n1),
    "order_date": pd.to_datetime("2026-01-01")
    + pd.to_timedelta(rng1.integers(0, 180, n1), unit="D"),
    "branch": rng1.choice(
        ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"],
        n1,
        p=[0.4, 0.2, 0.15, 0.15, 0.1],
    ),
    "product": rng1.choice(list(products), n1),
    "quantity": rng1.integers(1, 6, n1),
    "channel": rng1.choice(
        ["In-store", "Online", "Phone order"], n1, p=[0.55, 0.35, 0.10]
    ),
})
sales["unit_price"] = sales["product"].map(products)
sales.to_csv("duka_sales.csv", index=False)
print("duka_sales.csv generated.")

# Generator 2: Mobile Money Agent Network
rng2 = np.random.default_rng(44)
n2 = 600
agents = pd.DataFrame({
    "agent_id": [f"AG{i:03d}" for i in range(1, 21)],
    "county": rng2.choice(
        ["Nairobi", "Kiambu", "Nakuru", "Mombasa", "Kisumu"], 20
    ),
    "onboarded": pd.date_range("2024-01-01", periods=20, freq="MS").strftime(
        "%Y-%m-%d"
    ),
})
txns = pd.DataFrame({
    "txn_id": [f"TX{i:05d}" for i in range(1, n2 + 1)],
    "agent_id": rng2.choice(agents["agent_id"], n2),
    "txn_type": rng2.choice(
        ["Deposit", "withdrawal", "DEPOSIT ", "Withdrawal", "deposit"], n2
    ),
    "amount": rng2.lognormal(7.5, 0.8, n2).round(0).astype(str),
    "txn_date": (
        pd.to_datetime("2026-03-01")
        + pd.to_timedelta(rng2.integers(0, 60, n2), unit="D")
    ).strftime("%Y-%m-%d"),
})
idx = rng2.choice(n2, 30, replace=False)
txns.loc[idx[:15], "amount"] = np.nan
txns.loc[idx[15:20], "amount"] = "N/A"
txns.loc[idx[20:25], "amount"] = "250000"
txns.loc[idx[25:], "txn_date"] = txns.loc[idx[25:], "txn_date"].str.replace(
    "-", "/"
)
txns = pd.concat([txns, txns.sample(12, random_state=1)], ignore_index=True)
txns.loc[rng2.choice(len(txns), 8, replace=False), "agent_id"] = "AG099"
agents.to_csv("agents.csv", index=False)
txns.to_csv("agent_transactions.csv", index=False)
print("agents.csv and agent_transactions.csv generated.")
