import pandas as pd

# 1. Load the Gene Expression file
# Since it is a .txt file, it's likely tab-separated (\t)
df_expr = pd.read_csv('10_merged_174libs_0FPM kopie.txt', sep='\t')

# 2. List of your 5 winning predictor files
predictor_files = [
    'predictors_winners_0-index.csv',
    'predictors_winners_a-variance-descending.csv',
    'predictors_winners_b-pearsonr-descending.csv',
    'predictors_winners_c-fewest-nonzero-predictors.csv',
    'predictors_winners_d-random.csv'
]

for file in predictor_files:
    try:
        # Load the specific predictor list for this method
        df_preds = pd.read_csv(file)
        
        # 3. MERGE: Match 'gdm_gene_id' from your list to 'Gene' in expression file
        # We do an 'inner' merge to only keep genes that exist in both files
        merged_data = df_preds.merge(df_expr, left_on='gdm_gene_id', right_on='Gene', how='inner')
        
        # 4. CLEANUP: Remove the GDM ID and the redundant 'Gene' column
        # We only want Entrez ID + all the sample expression columns
        # We drop 'gdm_gene_id', 'Gene', and 'cluster' (unless you want to keep cluster)
        cols_to_drop = ['gdm_gene_id', 'Gene', 'cluster']
        final_expression_df = merged_data.drop(columns=cols_to_drop)
        
        # 5. SAVE: Create the new expression-only file
        output_name = file.replace('predictors_winners_', 'expression_values_')
        final_expression_df.to_csv(output_name, index=False)
        
        print(f"Created {output_name}: {len(final_expression_df)} genes matched.")
        
    except FileNotFoundError:
        print(f"Warning: Could not find {file}, skipping.")