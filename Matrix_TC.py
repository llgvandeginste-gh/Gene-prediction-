import pandas as pd

# 1. Load the big data file (Tab-separated)
# '\t' is the Python code for a Tab
big_df = pd.read_csv(r'C:\Users\ilseh\OneDrive\Documenten\Python\100par_matrix\dormouse_final_unique_with_coordinates_2 kopie.csv', sep='\t')

# 2. Load the small data file (Comma-separated)
# We use header=None because you mentioned it doesn't have one
small_df = pd.read_csv(r'C:\Users\ilseh\OneDrive\Documenten\Python\100par_matrix\matrix_cluster_1_filtered.csv', sep=',', header=None)

# 3. Define your column names
# Replace these with the exact names from your big file's header
gene_col = 'dormouse_id'
id_col = 'entrezgene_id_human'

# 4. Rename the first column of the small file so pandas knows what to match on
small_df = small_df.rename(columns={0: gene_col})

# 5. Clean up any accidental whitespace (common in tab-separated files)
big_df.columns = big_df.columns.str.strip()
big_df[gene_col] = big_df[gene_col].astype(str).str.strip()
small_df[gene_col] = small_df[gene_col].astype(str).str.strip()

# 6. Extract only the mapping columns from the big file
mapping_subset = big_df[[gene_col, id_col]]

# 7. Merge - this adds the ID column to the small file based on the gene name
result = pd.merge(small_df, mapping_subset, on=gene_col, how='left')

# 8. Save the result
result.to_csv('merged_output.csv', index=False)

print("Success! The files have been merged into 'merged_output.csv'.")