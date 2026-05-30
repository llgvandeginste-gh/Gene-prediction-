import pandas as pd

# 1. Load the Master List created in the previous step
df = pd.read_csv('dormouse_complete_30000_traceability_list_1.csv')

# Define target columns for checking empty values
mouse_col = 'mouse_gene_id'
human_col = 'entrezgene_id_human'

# --- SUBSET 1: NOT KNOWN IN MICE OR HUMAN ---
df_unknown_all = df[df[mouse_col].isna() & df[human_col].isna()].copy()

# --- SUBSET 2: KNOWN IN MICE BUT NOT IN HUMAN ---
df_mouse_only = df[df[mouse_col].notna() & df[human_col].isna()].copy()

# --- SUBSET 3: KNOWN IN HUMAN ---
df_known_human = df[df[human_col].notna()].copy()

# --- SAVE FILES ---
df_unknown_all.to_csv('dormouse_subset_unknown_all_1.csv', index=False)
df_mouse_only.to_csv('dormouse_subset_mouse_onl_1.csv', index=False)
df_known_human.to_csv('dormouse_subset_known_human_1.csv', index=False)

# --- Number check ---
print("--- SUBSET GENERATION SUMMARY ---")
print(f"1. Unknown to Both:         {len(df_unknown_all)} rows")
print(f"2. Known Mouse / No Human:  {len(df_mouse_only)} rows")
print(f"3. Known Human (with dupes): {len(df_known_human)} rows")
