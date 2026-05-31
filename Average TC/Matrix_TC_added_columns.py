import pandas as pd


df = pd.read_csv(r'C:\Users\ilseh\Downloads\ica_flipped_independent_components_consensus.tsv', sep='\t', index_col=0) 


# 1. Create the binary matrix (1 if >= 3, else 0)
binary_matrix = (df >= 3).astype(int)

# 2. Add 'Total_Above_3' column
binary_matrix['Total_Above_3'] = binary_matrix.sum(axis=1)

# 3. Add 'Any_Above_3' column
binary_matrix['Any_Above_3'] = (binary_matrix['Total_Above_3'] > 0).astype(int)

# 4. Save the final result to a new TSV file
binary_matrix.to_csv('gene_matrix_results.tsv', sep='\t')

print("gene_matrix_columns.tsv' has been created.")
