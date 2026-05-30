import pandas as pd

#load data
df_exp = pd.read_csv('/Users/familievandeginste/Documents/GeneIDs/10_merged_174libs_0FPM.txt', sep='\t')
#Add headers to dormouse to ensembl file
df_d_to_m = pd.read_csv('/Users/familievandeginste/Documents/GeneIDs/dormice_vs_ensembl_mouse_9t.tsv', 
                         sep='\t', header=None, usecols=[0, 1], names=['dormouse_gene_id', 'mouse_transcript_id'])
df_biomart = pd.read_csv('/Users/familievandeginste/Documents/GeneIDs/Biomart mouse transcript to hgnc.txt', sep='\t')

# Match names. Remove versions numbers of dormouse gene ids in dormice_vs_ensembl_mouse_9t.tsv file
def get_link_id(id_str):
    parts = str(id_str).split('.')
    return f"{parts[0]}.{parts[1]}" if len(parts) >= 2 else parts[0]


df_exp['link_id'] = df_exp['Gene'].apply(get_link_id)
df_d_to_m['link_id'] = df_d_to_m['dormouse_gene_id'].apply(get_link_id)

#Remove versions numbers ENSEMBLE IDs from dormouse_to_ensemble file
df_d_to_m['m_t_clean'] = df_d_to_m['mouse_transcript_id'].astype(str).str.split('.').str[0]
df_biomart['m_t_clean'] = df_biomart['ensembl_transcript_id'].astype(str).str.split('.').str[0]

df_shuffled = df_d_to_m.sample(frac=1, random_state=42)
df_biomart_shuffled = df_biomart.sample(frac=1, random_state=42)

#dropping duplicates in both ensembl and biomart file
df_mapping_unique = df_d_to_m.drop_duplicates(subset=['link_id'], keep='first').copy()

df_biomart_unique = df_biomart[['m_t_clean', 'ensembl_gene_id']].drop_duplicates(subset=['m_t_clean'])

# This is a Double Filter. A gene must:
# Exist in the Dormouse mapping.
# and have a valid Gene ID in the BiomaRt file.
# If it fails either condition, it is dropped
bridge_strict = pd.merge(df_mapping_unique, df_biomart_unique, on='m_t_clean', how='inner')

#creating dormouse_mouse_1to1_lookup table (=mouse known list of 18789)
final_lookup = pd.merge(df_exp[['Gene', 'link_id']], 
                        bridge_strict[['link_id', 'mouse_transcript_id', 'ensembl_gene_id']], 
                        on='link_id', 
                        how='inner')


final_lookup = final_lookup[['Gene', 'mouse_transcript_id', 'ensembl_gene_id']]
final_lookup.columns = ['dormouse_id', 'mouse_transcript_id', 'mouse_gene_id']

total_genes = len(df_exp)
known_mouse = len(final_lookup)
unknown = total_genes - known_mouse

print("--- REFINED FLOWCHART SUMMARY (STRICT GENE ID) ---")
print(f"Total Dormouse Genes:       {total_genes}")
print(f"Known Mouse Orthologs:      {known_mouse} (Must have Transcript AND Gene ID)")
print(f"Unknown Genes:              {unknown} (Includes those with Transcript but no Gene ID)")

final_lookup.to_csv('/Users/familievandeginste/Documents/GeneIDs/dormouse_to_mouse_1to1_complete_lookup_1.csv', index=False)

#creating unknown list
df_unknown_list = df_exp[~df_exp['Gene'].isin(final_lookup['dormouse_id'])][['Gene']].copy()

df_unknown_list.to_csv('/Users/familievandeginste/Documents/GeneIDs/dormouse_unknown_genes.csv', index=False)

print(f"Unknown genes saved: {len(df_unknown_list)} rows")