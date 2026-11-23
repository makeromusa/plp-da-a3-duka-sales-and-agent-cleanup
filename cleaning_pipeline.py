import numpy as np
import pandas as pd


def clean_agent_data(txns, agents):
  """Clean and standardize raw mobile money transactions and merge with agent register.

  Applies programmatic cleaning rules:
  1. Deduplicates transactions by txn_id.
  2. Standardizes txn_type to 'Deposit' and 'Withdrawal'.
  3. Coerces amount to numeric and imputes missing/invalid entries with the
  median.
  4. Standardizes txn_date to datetime (ISO format).
  5. Flags statistical outliers using the IQR rule (Q3 + 1.5 * IQR).
  6. Merges with agents register and labels unregistered agents as 'Unknown'.

  Parameters:
      txns (pd.DataFrame): Raw transaction records.
      agents (pd.DataFrame): Agent registration details.

  Returns:
      tuple: (clean_df, log) where clean_df is the processed DataFrame and log
      is a list of audit messages.
  """
  log = []
  init_len = len(txns)

  # 1. Deduplication on txn_id
  clean_df = txns.drop_duplicates(subset=["txn_id"]).copy()
  dups_removed = init_len - len(clean_df)
  log.append(f"Removed {dups_removed} duplicate transactions based on txn_id.")

  # 2. Standardize txn_type
  clean_df["txn_type"] = clean_df["txn_type"].astype(str).str.strip().str.title()
  log.append("Standardized txn_type into 'Deposit' and 'Withdrawal'.")

  # 3. Numeric conversion and median imputation for amount
  numeric_amount = pd.to_numeric(clean_df["amount"], errors="coerce")
  clean_df["amount_imputed"] = numeric_amount.isna()
  median_amount = float(numeric_amount.median())
  clean_df["amount"] = numeric_amount.fillna(median_amount)
  imputed_count = int(clean_df["amount_imputed"].sum())
  log.append(
      f"Imputed {imputed_count} missing/invalid amounts with median"
      f" (KES {median_amount:,.0f})."
  )

  # 4. Standardize txn_date to datetime
  clean_df["txn_date"] = pd.to_datetime(
      clean_df["txn_date"].astype(str).str.replace("/", "-")
  )
  log.append("Parsed and standardized txn_date to ISO datetime format.")

  # 5. Outlier detection via IQR
  q1 = float(clean_df["amount"].quantile(0.25))
  q3 = float(clean_df["amount"].quantile(0.75))
  iqr = q3 - q1
  upper_fence = q3 + 1.5 * iqr
  clean_df["is_outlier"] = clean_df["amount"] > upper_fence
  outlier_count = int(clean_df["is_outlier"].sum())
  log.append(
      f"Flagged {outlier_count} high-value outliers exceeding upper fence"
      f" KES {upper_fence:,.2f}."
  )

  # 6. Merge with agent register
  merged_df = clean_df.merge(
      agents[["agent_id", "county"]], on="agent_id", how="left"
  )
  unknown_agents = int(merged_df["county"].isna().sum())
  merged_df["county"] = merged_df["county"].fillna("Unknown")
  log.append(
      f"Merged with agent register; {unknown_agents} transactions with unknown"
      " agents assigned to 'Unknown' county."
  )

  return merged_df, log
