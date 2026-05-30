import pandas as pd

# 1. Load your clean matrix
matrix_path = r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\merged_matrix_entrezid_complete.csv'
df_matrix = pd.read_csv(matrix_path)

# 2. Load the TC file 
# tc_file_path = r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\TC_summary_only.tsv', sep='\t'
df_tc = pd.read_csv(r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\TC_summary_only.tsv', sep='\t')

# 3. Rename the columns based on the image
# Since the first column is blank in the screenshot, pandas calls it 'Unnamed: 0'
# We rename it to match your matrix's Entrez ID column name
df_tc = df_tc.rename(columns={
    df_tc.columns[0]: 'entrezgene_id_human',
    'Total_Above_3': 'TC'
})

# 4. Merge
df_final = df_matrix.merge(
    df_tc[['entrezgene_id_human', 'TC']], 
    on='entrezgene_id_human', 
    how='left'
)

# 5. Save
output_path = r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\merged_matrix_with_TC.csv'
df_final.to_csv(output_path, index=False)

print("Success! TC column attached and matched by Entrez ID.")
