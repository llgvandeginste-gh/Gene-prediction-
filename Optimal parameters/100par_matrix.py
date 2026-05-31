import pandas as pd
import os

# 1. Setup
base_path = r'/Users/familievandeginste/Documents/100par_matrix'
data_path = os.path.join(base_path, 'Renamed_Results_100par') 
clusters = [1, 2, 3]
methods = ['0', 'a', 'b', 'c', 'd']

def super_clean(text):
    return str(text).strip().replace('"', '').replace("'", "")

# 2. Process
for c in clusters:
    print(f"\nProcessing Cluster {c}...")
    
    # First pass: Find all unique genes across all files for this cluster
    all_observed_genes = set()
    prefix_cluster = f"predictor_names_{c}_"
    cluster_files = [f for f in os.listdir(data_path) if f.startswith(prefix_cluster) and f.endswith(".txt")]
    
    if not cluster_files:
        print(f"  No files found for Cluster {c}. Skipping.")
        continue

    for f_name in cluster_files:
        with open(os.path.join(data_path, f_name), 'r') as f:
            content = f.read().replace(',', ' ').split()
            genes = [super_clean(w) for w in content if w.strip()]
            all_observed_genes.update(genes)
    
    # Sort genes alphabetically for a consistent row order
    sorted_genes = sorted(list(all_observed_genes))
    gene_to_idx = {gene: i for i, gene in enumerate(sorted_genes)}
    
    cluster_data = {}

    # Second pass: Fill the matrix
    for m in methods:
        prefix_method = f"predictor_names_{c}_{m}_"
        # Get parameter files and sort them (e.g., 0.001 comes before 0.01)
        param_files = sorted([f for f in cluster_files if f.startswith(prefix_method)])

        for pred_file in param_files:
            params = pred_file.replace(prefix_method, "").replace(".txt", "")
            column_name = f"method_{m}_{params}"
            
            # Initialize column with zeros for only observed genes
            col_values = [0] * len(sorted_genes)
            
            with open(os.path.join(data_path, pred_file), 'r') as f:
                content = f.read().replace(',', ' ').split()
                preds_in_file = [super_clean(w) for w in content if w.strip()]
                
                for p in preds_in_file:
                    if p in gene_to_idx:
                        col_values[gene_to_idx[p]] = 1
            
            cluster_data[column_name] = col_values

    # 3. Save
    if cluster_data:
        df = pd.DataFrame(cluster_data, index=sorted_genes)
        output_name = f"matrix_cluster_{c}_filtered.csv"
        df.to_csv(os.path.join(base_path, output_name))
        print(f"  Saved: {output_name} ({len(sorted_genes)} genes x {len(df.columns)} columns)")

print("\nProcessing complete.")