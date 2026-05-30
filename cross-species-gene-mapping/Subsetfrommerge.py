import pandas as pd

# 1. Load the combined file (Randomly resolved Multi + Single mapped)
df = pd.read_csv('dormouse_known_human_final_1to1_list_1.csv')

# 2. Count occurrences of each Human ID
# This tells us if multiple Dormouse genes are sharing the same Human ortholog
human_counts = df['entrezgene_id_human'].value_counts()

# Identify Human IDs used more than once
colliding_human_ids = human_counts[human_counts > 1].index

# --- SUBSET 1: MANY-TO-ONE (COLLISIONS) ---
# All rows where the Human ID is shared by multiple Dormouse genes
df_many_to_one = df[df['entrezgene_id_human'].isin(colliding_human_ids)].copy()
df_many_to_one = df_many_to_one.sort_values(by='hgnc_symbol_human')

# --- SUBSET 2: TRUE 1-TO-1 ---
# Rows where the Human ID is unique to exactly one Dormouse gene
df_true_1to1 = df[~df['entrezgene_id_human'].isin(colliding_human_ids)].copy()
df_true_1to1 = df_true_1to1.sort_values(by='dormouse_id')

# --- SAVE RESULT ---
df_many_to_one.to_csv('dormouse_to_human_many_to_one_collisions_1.csv', index=False)
df_true_1to1.to_csv('dormouse_to_human_true_1to1_unique_1.csv', index=False)

# --- FINAL REPORT ---
print("\n" + "="*45)
print("--- TOPOLOGY SPLIT SUMMARY ---")
print(f"Total entries analyzed:            {len(df)}")
print("-" * 45)
print(f"TRUE 1-to-1 Subset:                {len(df_true_1to1)} genes")
print(f"MANY-to-One Subset (Collisions):   {len(df_many_to_one)} rows")
print(f"   └─ involving {len(colliding_human_ids)} distinct Human IDs")
print("-" * 45)
print("Files saved: ")
print(" - dormouse_to_human_true_1to1_unique.csv")
print(" - dormouse_to_human_many_to_one_collisions.csv")
print("="*45)