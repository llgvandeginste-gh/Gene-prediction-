import pandas as pd

# Load the final merged file
file_path = 'matrix_entrezid_1.csv'
df = pd.read_csv(file_path, index_col=0)

print(df.shape)

# 1. Check for Missing IDs (Completeness)
missing_count = df['entrezgene_id_human'].isna().sum()
total_rows = len(df)
percent_missing = (missing_count / total_rows) * 100

print("--- COMPLETENESS CHECK ---")
print(f"Total Genes: {total_rows}")
print(f"Genes missing a Human Entrez ID: {missing_count} ({percent_missing:.2f}%)")

# 2. Check for Unique IDs (Uniqueness)
# We ignore NaNs for the uniqueness check since they are expected to be "duplicates"
unique_ids = df['entrezgene_id_human'].dropna().nunique()
total_non_null_ids = df['entrezgene_id_human'].dropna().count()
duplicates_count = total_non_null_ids - unique_ids

print("\n--- UNIQUENESS CHECK ---")
print(f"Total Human IDs assigned: {total_non_null_ids}")
print(f"Unique Human IDs: {unique_ids}")
print(f"Duplicate assignments: {duplicates_count}")

if duplicates_count > 0:
    print("\nTop 5 duplicated Human IDs (and how many dormouse genes they map to):")
    print(df['entrezgene_id_human'].value_counts().head(5))

 # Filter the dataframe to show only the row with the missing ID
missing_row = df[df['entrezgene_id_human'].isna()]

# Display the gdm_gene_id (the index) and the Cluster it belongs to
print("The missing gene is:")
print(missing_row)

import pandas as pd

# 1. Load the file, skipping the "row of numbers"
# header=1 tells pandas that the REAL headers are on the second line
file_path = '/Users/familievandeginste/Documents/100par_matrix/matrix_entrezid_1.csv'
df = pd.read_csv(file_path, header=1)

# 2. Fix the names of the first and last columns 
# Because we skipped the first row, these two specific names got lost
cols = list(df.columns)
cols[0] = 'dormouse_id'           # Rename the first column
cols[-1] = 'entrezgene_id_human' # Rename the last column
df.columns = cols

# 3. Save it
df.to_csv('/Users/familievandeginste/Documents/100par_matrix/matrix_entrezid_1_1', index=False)

print("Done! Numbers removed and headers aligned.")