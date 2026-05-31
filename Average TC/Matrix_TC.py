import pandas as pd


big_df = pd.read_csv(r'C:\Users\ilseh\OneDrive\Documenten\Python\100par_matrix\dormouse_final_unique_with_coordinates_2 kopie.csv', sep='\t')

small_df = pd.read_csv(r'C:\Users\ilseh\OneDrive\Documenten\Python\100par_matrix\matrix_cluster_1_filtered.csv', sep=',', header=None)

gene_col = 'dormouse_id'
id_col = 'entrezgene_id_human'

small_df = small_df.rename(columns={0: gene_col})

big_df.columns = big_df.columns.str.strip()
big_df[gene_col] = big_df[gene_col].astype(str).str.strip()
small_df[gene_col] = small_df[gene_col].astype(str).str.strip()

mapping_subset = big_df[[gene_col, id_col]]

result = pd.merge(small_df, mapping_subset, on=gene_col, how='left')

result.to_csv('merged_output.csv', index=False)

print("The files have been merged into 'merged_output.csv'.")
