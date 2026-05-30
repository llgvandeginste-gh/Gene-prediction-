import pandas as pd

# 1. Load your datafile (TSV format)
# Ensure 'your_data.tsv' is the name of your actual file
df = pd.read_csv(r'C:\Users\ilseh\Downloads\ica_flipped_independent_components_consensus.tsv', sep='\t', index_col=0) 

print("Processing data...")

# 2. Create the binary matrix (1 if >= 3, else 0)
binary_matrix = (df >= 3).astype(int)

# 3. Add 'Total_Above_3' column
# This counts how many 1s are in each row
binary_matrix['Total_Above_3'] = binary_matrix.sum(axis=1)

# 4. Add 'Any_Above_3' column
# This puts a 1 if the 'Total_Above_3' is at least 1, otherwise 0
binary_matrix['Any_Above_3'] = (binary_matrix['Total_Above_3'] > 0).astype(int)

# 5. Save the final result to a new TSV file
binary_matrix.to_csv('gene_matrix_results.tsv', sep='\t')

print("Success! 'gene_matrix_columns.tsv' has been created.")