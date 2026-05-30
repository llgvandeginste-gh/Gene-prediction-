import pandas as pd

# 1. Load the list of unique dormouse IDs
df_unique = pd.read_csv('dormouse_final_consolidated_unique_genes.csv')
unique_ids = df_unique['dormouse_id'].unique()

# 2. Load the expression file
df_exp = pd.read_csv('10_merged_174libs_0FPM.txt', sep='\t')

# 3. Filter the expression file to keep only the unique IDs
# The expression file uses the column name 'Gene' for the IDs
df_filtered_exp = df_exp[df_exp['Gene'].isin(unique_ids)].copy()

# 4. Save the result
# This file will contain the 'Gene' column plus all sample expression columns
output_name = 'unique_genes_expression_only.csv'
df_filtered_exp.to_csv(output_name, index=False)

print("-" * 30)
print(f"Extraction Complete!")
print(f"Total Unique Genes: {len(unique_ids)}")
print(f"Genes found in expression data: {len(df_filtered_exp)}")
print(f"Saved to: {output_name}")
print("-" * 30)