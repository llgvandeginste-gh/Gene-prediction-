import pandas as pd

matrix_path = r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\merged_matrix_entrezid_complete.csv'
df_matrix = pd.read_csv(matrix_path)


# tc_file_path = r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\TC_summary_only.tsv', sep='\t'
df_tc = pd.read_csv(r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\TC_summary_only.tsv', sep='\t')

# 1. Rename the columns
df_tc = df_tc.rename(columns={
    df_tc.columns[0]: 'entrezgene_id_human',
    'Total_Above_3': 'TC'
})

# 2. Merge
df_final = df_matrix.merge(
    df_tc[['entrezgene_id_human', 'TC']], 
    on='entrezgene_id_human', 
    how='left'
)

# 3. Save
output_path = r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\merged_matrix_with_TC.csv'
df_final.to_csv(output_path, index=False)

print("TC column attached and matched by Entrez ID.")
