import pandas as pd
import numpy as np
import requests
import gzip
import io

# --- PART 1: GENOME MAPPING & CLEANING ---
print("Step 1: Mapping Dormouse to Human...")
df_lookup = pd.read_csv('/Users/familievandeginste/Documents/GeneIDs/dormouse_to_mouse_1to1_complete_lookup.csv')
df_ortho = pd.read_csv('/Users/familievandeginste/Documents/GeneIDs/Mouse to human orthologs homologs biomaRt distinct human (1).txt')

# Clean strings to ensure matches
df_lookup['mouse_gene_id'] = df_lookup['mouse_gene_id'].astype(str).str.strip()
df_ortho['ensemblgene_id_mouse'] = df_ortho['ensemblgene_id_mouse'].astype(str).str.strip()

# Initial Merge
df_map_raw = pd.merge(df_lookup, df_ortho, left_on='mouse_gene_id', right_on='ensemblgene_id_mouse', how='inner')

# --- UNBIASED SELECTION LOGIC ---
# 1. Identify the confidence column dynamically
conf_col = [c for c in df_map_raw.columns if '"mouse_orthology_confidence_[0_low,_1_high]"' in c.lower()]

if conf_col:
    conf_col = conf_col[0]
    print(f"Applying unbiased selection using {conf_col}...")
    
    # 2. Add a temporary random column to break ties between identical confidence scores
    # This removes the alphabetical bias found in the raw source file[cite: 1]
    np.random.seed(42) # Seed 42 for reproducibility
    df_map_raw['temp_random'] = np.random.rand(len(df_map_raw))
    
    # 3. Sort: Dormouse ID (Ascending), Confidence (Descending), Random (Ascending)
    df_map = df_map_raw.sort_values(
        by=['dormouse_id', conf_col, 'temp_random'], 
        ascending=[True, False, True]
    )
    
    # 4. Keep the 'winner' for each dormouse ID
    df_map = df_map.drop_duplicates(subset=['dormouse_id'], keep='first')
    
    # Clean up the temporary column
    df_map = df_map.drop(columns=['temp_random'])
else:
    print("Warning: Confidence column not found. Performing full random shuffle.")
    df_map = df_map_raw.sample(frac=1, random_state=42).drop_duplicates(subset=['dormouse_id'], keep='first')

# Save the master mapping file
df_map.to_csv('dormouse_mouse_human_detailed_mapping_unbiased.csv', index=False)

# Identify those without orthologs for the final math summary
df_no_human = df_lookup[~df_lookup['dormouse_id'].isin(df_map['dormouse_id'])].copy()

# --- PART 2: CORRELATION ANALYSIS ---
print("Step 2: Analyzing Expression Correlations...")
df_exp = pd.read_csv('/Users/familievandeginste/Documents/GeneIDs/10_merged_174libs_0FPM kopie.txt', sep='\t')

# Find multi-gene clusters (Dormouse genes sharing a Human ortholog)
ortho_groups = df_map.groupby('hgnc_symbol_human')['dormouse_id'].apply(list)
multi_gene_groups = ortho_groups[ortho_groups.apply(len) > 1]

all_pairs_results = []
exp_numeric = df_exp.set_index('Gene').select_dtypes(include=[np.number])

for human_gene, dormouse_list in multi_gene_groups.items():
    present_genes = exp_numeric.index.intersection(dormouse_list)
    subset = exp_numeric.loc[present_genes].T
    
    if subset.shape[1] > 1:
        corr_matrix = subset.corr()
        mask = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        avg_corr = corr_matrix.where(mask).stack().mean()
        all_pairs_results.append({'human_ortholog': human_gene, 'dormouse_genes': dormouse_list, 'avg_pearson_r': avg_corr})

df_corr = pd.DataFrame(all_pairs_results)

# --- PART 3: CATEGORIZATION ---
print("Step 3: Categorizing Redundant vs Diverged...")
redundant_to_remove = set()
all_diverged_genes = set()

for _, row in df_corr.iterrows():
    cluster = row['dormouse_genes']
    if row['avg_pearson_r'] >= 0.9:
        redundant_to_remove.update(cluster[1:]) # Keep first based on file order, remove others
    else:
        all_diverged_genes.update(cluster) # Keep all as 'Diverged'

# --- PART 4: FINAL FILE CREATION ---
ids_not_unique = redundant_to_remove.union(all_diverged_genes)

df_unique = df_map[~df_map['dormouse_id'].isin(ids_not_unique)].copy()
df_not_unique = df_map[df_map['dormouse_id'].isin(ids_not_unique)].copy()

# --- PART 5: COORDINATE RETRIEVAL ---
print("Step 4: Fetching Human Coordinates...")
entrez_col = 'entrezgene_id_human'
df_unique[entrez_col] = pd.to_numeric(df_unique[entrez_col], errors='coerce').fillna(0).astype(int).astype(str)
target_entrez = set(df_unique[entrez_col].unique())

gff_url = "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_genomic.gff.gz"
gene_coords = []
response = requests.get(gff_url, stream=True)
with gzip.open(io.BytesIO(response.content), 'rt') as f:
    for line in f:
        if line[0] == '#' or '\tgene\t' not in line: continue
        parts = line.split('\t')
        if 'GeneID:' in parts[8]:
            eid = parts[8].split('GeneID:')[1].split(',')[0].split(';')[0]
            if eid in target_entrez and 'NC_' in parts[0]:
                gene_coords.append({'GeneID': eid, 'Chromosome': parts[0], 'BP_Start': parts[3], 'BP_End': parts[4], 'Strand': parts[6]})

coords_lookup = pd.DataFrame(gene_coords).drop_duplicates(subset=['GeneID'])
final_unique_df = pd.merge(df_unique, coords_lookup, left_on=entrez_col, right_on='GeneID', how='left')

# Save Results
final_unique_df.to_csv('dormouse_unique_genes_unbiased_final.csv', index=False)
df_not_unique.to_csv('dormouse_not_unique_genes_unbiased_final.csv', index=False)

# --- FINAL SUMMARY ---
print("\n" + "="*40)
print("--- FINAL MAPPING SUMMARY (UNBIASED) ---")
print(f"Total Dormouse IDs processed:    {len(df_lookup)}")
print(f"  ├─ Unique Genes Saved:         {len(df_unique)}")
print(f"  └─ Not Unique Genes Total:     {len(df_not_unique)}")
print(f"Genes without Human Orthologs:   {len(df_no_human)}")
print("-" * 40)
total_math = len(df_unique) + len(df_not_unique) + len(df_no_human)
print(f"Math Check: {len(df_unique)} + {len(df_not_unique)} + {len(df_no_human)} = {total_math}")
print("="*40)
