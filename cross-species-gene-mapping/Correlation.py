import pandas as pd
import numpy as np

# 1. Load the data
df_many = pd.read_csv('dormouse_to_human_many_to_one_collisions.csv')
df_exp = pd.read_csv('10_merged_174libs_0FPM.txt', sep='\t')

# Prepare numeric expression data
exp_numeric = df_exp.set_index('Gene').select_dtypes(include=[np.number])

# 2. Group by Human Ortholog
ortho_groups = df_many.groupby('hgnc_symbol_human')['dormouse_id'].apply(list)

redundant_ids = set()    
diverged_ids = set()     
unique_winner_ids = []   
correlation_data = []    

# Set seed for reproducibility
np.random.seed(42)

# 3. Iterate through clusters
for human_gene, dormouse_list in ortho_groups.items():
    present_genes = exp_numeric.index.intersection(dormouse_list).tolist()
    
    if len(present_genes) > 1:
        subset = exp_numeric.loc[present_genes].T
        corr_matrix = subset.corr()
        
        mask = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        avg_r = corr_matrix.where(mask).stack().mean()
        
        correlation_data.append({'human_ortholog': human_gene, 'avg_r': avg_r, 'cluster_size': len(present_genes)})
        
        if avg_r >= 0.9:
            # CATEGORY: REDUNDANT
            # --- RANDOM SELECTION LOGIC ---
            # Shuffle the list of present genes randomly
            np.random.shuffle(present_genes)
            # The first one in the shuffled list is our random winner
            winner = present_genes[0]
            others = present_genes[1:]
            
            unique_winner_ids.append(winner)
            redundant_ids.update(others)
        else:
            # CATEGORY: DIVERGED
            diverged_ids.update(present_genes)
            
    elif len(present_genes) == 1:
        unique_winner_ids.append(present_genes[0])

# 4. Create the final DataFrames
df_unique = df_many[df_many['dormouse_id'].isin(unique_winner_ids)].copy()
df_redundant = df_many[df_many['dormouse_id'].isin(redundant_ids)].copy()
df_diverged = df_many[df_many['dormouse_id'].isin(diverged_ids)].copy()
df_not_unique = pd.concat([df_redundant, df_diverged]).drop_duplicates()

# 5. Save all files
df_unique.to_csv('many_to_one_unique_winners_random_1.csv', index=False)
# df_not_unique.to_csv('many_to_one_not_unique_all.csv', index=False)
# df_redundant.to_csv('many_to_one_redundant_only.csv', index=False)
# df_diverged.to_csv('many_to_one_diverged_only.csv', index=False)

print("\n" + "="*45)
print("--- UNBIASED CORRELATION SUMMARY ---")
print(f"Unique Winners (Randomly picked): {len(df_unique)}")
print(f"Redundant Copies (Discarded):     {len(df_redundant)}")
print(f"Diverged Genes (Kept separate):   {len(df_diverged)}")
print("="*45)