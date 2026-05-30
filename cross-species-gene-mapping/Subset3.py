import pandas as pd

# Load the multi-mapped genes file
df_multi = pd.read_csv('dormouse_known_human_multi_mapped.csv')

# Define the exact confidence column name
conf_col = "mouse_orthology_confidence_[0_low,_1_high]"

# 1. Subset rows with score 1.0
df_score_1 = df_multi[df_multi[conf_col] == 1].copy()

# 2. Subset rows with score 0
df_score_0 = df_multi[df_multi[conf_col] == 0].copy()

# 3. Find unique Garden Dormouse IDs in each set
ids_with_1 = set(df_score_1['dormouse_id'].unique())
ids_with_0 = set(df_score_0['dormouse_id'].unique())

# 4. Find the overlap (Dormouse IDs that appear in both sets)
overlap_ids = ids_with_1.intersection(ids_with_0)

# --- SAVE FILES ---
df_score_1.to_csv('multimapped_rows_score_1.csv', index=False)
df_score_0.to_csv('multimapped_rows_score_0.csv', index=False)

# Save the full rows for the overlap cases for detailed inspection
df_overlap = df_multi[df_multi['dormouse_id'].isin(overlap_ids)].copy()
df_overlap = df_overlap.sort_values(by='dormouse_id')
df_overlap.to_csv('multimapped_overlap_mixed_confidence.csv', index=False)

# --- REPORT ---

print("--- Overlap ---")
print(f"Genes with at least one score 1.0:    {len(ids_with_1)}")
print(f"Genes with at least one score 0:      {len(ids_with_0)}")
print(f"GENES WITH BOTH 1.0 AND 0 (OVERLAP):  {len(overlap_ids)}")
