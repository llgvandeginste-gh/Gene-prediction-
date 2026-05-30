import pandas as pd

# 1. Load the multi-mapped genes file
df_multi = pd.read_csv('dormouse_known_human_multi_mapped_1.csv')

# 2. Randomly shuffle the entire dataframe
# frac=1 shuffles all rows. random_state=42 makes it reproducible.
df_shuffled = df_multi.sample(frac=1, random_state=42).reset_index(drop=True)

# 3. Drop duplicates to keep only the first (now random) human match per dormouse gene
df_random_1to1 = df_shuffled.drop_duplicates(subset=['dormouse_id'], keep='first')

# 4. Sort by ID for organization
df_random_1to1 = df_random_1to1.sort_values(by='dormouse_id')

# --- SAVE RESULT ---
output_file = 'dormouse_multimapped_random_1to1_subset_1.csv'
df_random_1to1.to_csv(output_file, index=False)

# --- REPORT ---
print("\n" + "="*45)
print("--- RANDOM 1-to-1 SELECTION SUMMARY ---")
print(f"Original Multi-mapped Rows:       {len(df_multi)}")
print(f"Unique Dormouse Genes selected:   {len(df_random_1to1)}")
print("-" * 45)
print(f"File saved: {output_file}")
print("="*45)