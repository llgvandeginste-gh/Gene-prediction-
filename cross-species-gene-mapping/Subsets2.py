import pandas as pd


df_known = pd.read_csv('dormouse_subset_known_human_1.csv')

# 2. Identify which garden dormouse IDs map to multiple rows

id_counts = df_known['dormouse_id'].value_counts()
multi_mapped_ids = id_counts[id_counts > 1].index

# --- SUBSET A: MULTI-MAPPED GENES ---
df_multi = df_known[df_known['dormouse_id'].isin(multi_mapped_ids)].copy()

# --- SUBSET B: SINGLE-MAPPED GENES ---
# The rest: genes that appear exactly once
df_single = df_known[~df_known['dormouse_id'].isin(multi_mapped_ids)].copy()

# 3. Sort 
df_multi = df_multi.sort_values(by='dormouse_id')
df_single = df_single.sort_values(by='dormouse_id')

# --- SAVE FILES ---
df_multi.to_csv('dormouse_known_human_multi_mapped_1.csv', index=False)
df_single.to_csv('dormouse_known_human_single_mapped_1.csv', index=False)

# --- REPORT ---
print("\n" + "="*40)
print("--- KNOWN-IN-HUMAN SPLIT SUMMARY ---")
print(f"Total Unique Genes:         {df_known['dormouse_id'].nunique()}")
print("-" * 40)
print(f"Subset A (Multi-mapped):    {len(df_multi)} rows")
print(f"   └─ representing {len(multi_mapped_ids)} unique IDs")
print(f"Subset B (Single-mapped):   {len(df_single)} rows")
print("="*40)