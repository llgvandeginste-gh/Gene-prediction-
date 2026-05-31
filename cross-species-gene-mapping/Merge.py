import pandas as pd

# 1. Load the two "Known-in-Human" components
# Part A: The ones that had multiple options, now reduced to 1 randomly
df_random = pd.read_csv('dormouse_multimapped_random_1to1_subset_1.csv')

# Part B: The ones that only ever had one option
df_single = pd.read_csv('dormouse_known_human_single_mapped_1.csv')

# 2. Combine them vertically (stack them)
# pd.concat is used because we are adding rows, not matching columns
df_final_known = pd.concat([df_random, df_single], ignore_index=True)

# 3. Sort by Dormouse ID for final order
df_final_known = df_final_known.sort_values(by='dormouse_id')

# --- SAVE FINAL RESULT ---
output_file = 'dormouse_known_human_final_1to1_list_1.csv'
df_final_known.to_csv(output_file, index=False)

# --- FINAL VERIFICATION REPORT ---
print("\n" + "="*45)
print("--- FINAL 'KNOWN-IN-HUMAN' COMBINATION ---")
print(f"Clean 1-to-1 Genes:           {len(df_single)}")
print(f"Randomly resolved Genes:      {len(df_random)}")
print("-" * 45)
print(f"TOTAL FINAL 1-to-1 LIST:      {len(df_final_known)}")
print(f"Unique Dormouse ID Check:     {df_final_known['dormouse_id'].nunique()}")
print("-" * 45)
print(f"File saved: {output_file}")
print("="*45)
