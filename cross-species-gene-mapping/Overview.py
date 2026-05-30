import pandas as pd


df_exp = pd.read_csv('/Users/familievandeginste/Documents/GeneIDs/10_merged_174libs_0FPM.txt', sep='\t')
df_all_dormouse = df_exp[['Gene']].copy()
df_all_dormouse.rename(columns={'Gene': 'dormouse_id'}, inplace=True)

# 2. The Lookup File (Dormouse to Mouse)
df_lookup = pd.read_csv('dormouse_to_mouse_1to1_complete_lookup_1.csv')

# 3.Mouse to Human
df_ortho = pd.read_csv('/Users/familievandeginste/Documents/GeneIDs/Mouse to human orthologs homologs biomaRt distinct human (2).txt')

# --- CLEAN STRINGS ---
df_all_dormouse['dormouse_id'] = df_all_dormouse['dormouse_id'].astype(str).str.strip()
df_lookup['dormouse_id'] = df_lookup['dormouse_id'].astype(str).str.strip()
df_lookup['mouse_gene_id'] = df_lookup['mouse_gene_id'].astype(str).str.strip()
df_ortho['ensemblgene_id_mouse'] = df_ortho['ensemblgene_id_mouse'].astype(str).str.strip()

#  merge

df_step1 = pd.merge(df_all_dormouse, df_lookup, on='dormouse_id', how='left')


df_master = pd.merge(
    df_step1, 
    df_ortho, 
    left_on='mouse_gene_id', 
    right_on='ensemblgene_id_mouse', 
    how='left'
)


conf_col = "mouse_orthology_confidence_[0_low,_1_high]"

final_columns = [
    'dormouse_id', 
    'mouse_gene_id', 
    'entrezgene_id_human', 
    'hgnc_symbol_human', 
    conf_col
]

df_report = df_master[final_columns].copy()

# Sort 
df_report = df_report.sort_values(by=['dormouse_id'])

# RESULT
output_file = 'dormouse_complete_30000_traceability_list_1.csv'
df_report.to_csv(output_file, index=False)

# SUMMARY 
print("\n" + "="*40)
print("--- MASTER LIST ---")
print(f"Total rows (with duplicates): {len(df_report)}")
print(f"Total Dormouse IDs included:  {df_report['dormouse_id'].nunique()}")
print(f"File saved as:                {output_file}")
print("="*40)