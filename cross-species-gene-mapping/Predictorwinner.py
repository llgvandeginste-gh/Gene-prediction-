import pandas as pd

# 1. Load the files
df_winners = pd.read_csv('top_15_tc_winners.csv')
# Using semicolon separator based on your example
df_matrix = pd.read_csv('merged_cluster_matrix_entrezid.csv', sep=';')

# --- CLEANUP ---
df_matrix.columns = df_matrix.columns.str.strip()

# Ensure the 'Cluster' column in the matrix is treated as an integer for matching
df_matrix['Cluster'] = pd.to_numeric(df_matrix['Cluster'], errors='coerce')

# Target ID columns
target_ids = ['gdm_gene_id', 'entrezgene_id_human']
actual_ids = [c for c in df_matrix.columns if c in target_ids]

# Process each method (0, a, b, c, d)
for method_full in df_winners['ordering_method'].unique():
    method_results = []
    
    # Get the 3 winners for this method (one per cluster)
    winners_subset = df_winners[df_winners['ordering_method'] == method_full]
    
    for _, row in winners_subset.iterrows():
        winning_cluster = int(row['cluster'])
        m_short = f"method_{method_full.split('_')[0]}"
        
        # Build the exact column name
        t, g, s = str(row['tolerance']), str(row['gain_threshold']), str(row['score_threshold'])
        col_to_find = f"{m_short}_{t}tol_{g}gain_{s}score"
        
        if col_to_find in df_matrix.columns:
            # LOGIC:
            # 1. Column value must be 1 (as string or number)
            # 2. Matrix 'Cluster' column must match the Winner's Cluster
            mask = (
                ((df_matrix[col_to_find].astype(str) == '1') | (df_matrix[col_to_find] == 1)) & 
                (df_matrix['Cluster'] == winning_cluster)
            )
            
            # Extract the data
            cluster_genes = df_matrix.loc[mask, actual_ids].copy()
            
            # Add metadata for clarity
            cluster_genes['cluster'] = winning_cluster
            cluster_genes['params_used'] = col_to_find
            
            method_results.append(cluster_genes)
            print(f"Cluster {winning_cluster} for {m_short}: Found {len(cluster_genes)} genes.")
        else:
            print(f"Error: Column {col_to_find} not found in matrix.")

    # 3. Save the merged file for the method
    if method_results:
        final_df = pd.concat(method_results, ignore_index=True)
        # Keep only the requested columns
        final_output = final_df[actual_ids + ['cluster']]
        
        filename = f"predictors_winners_{method_full.replace('_', '-')}.csv"
        final_output.to_csv(filename, index=False)
        print(f"--- SUCCESS: Created {filename} ({len(final_output)} total rows) ---\n")