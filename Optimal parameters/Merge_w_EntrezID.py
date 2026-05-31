import pandas as pd

# Load the files
# Replace 'file1.csv' and 'file2.csv' with your actual filenames
df1 = pd.read_csv('merged_clusters_matrix.csv')
df2 = pd.read_csv('dormouse_final_unique_with_coordinates_2.csv', sep = '\t')

import pandas as pd

print(df2.columns.tolist())


# 1. Take only the columns you need
df2_subset = df2[['dormouse_id', 'entrezgene_id_human']].copy()

# 2. Rename 'dormouse_id' to match 'gdm_gene_id'
df2_subset.rename(columns={'dormouse_id': 'gdm_gene_id'}, inplace=True)

# 3. Merge on the shared name
# Because the names match, you only need 'on' and no extra column is created
merged_df = pd.merge(df1, df2_subset, on='gdm_gene_id', how='left')



# Save the result
merged_df.to_csv('merged_cluster_matrix_entrezid', index=False)

    
