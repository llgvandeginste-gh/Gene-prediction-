import pandas as pd
import os


base_path = r'/Users/familievandeginste/Documents/Predictors_responders'
data_path = os.path.join(base_path, 'Predictors') # The subfolder
clusters = [1, 2, 3]
methods = ['0', 'a', 'b', 'c', 'd']
runs = range(1, 11)

def super_clean(text):
    return str(text).strip().replace('"', '').replace("'", "")

# 1. Process
for c in clusters:
    # Load the clean gene list for this cluster
    master_txt = os.path.join(base_path, f"gene_list_cluster_{c}.txt")
    
    if not os.path.exists(master_txt):
        print(f"Skipping Cluster {c}: {master_txt} not found.")
        continue

    with open(master_txt, 'r') as f:
        master_genes = [super_clean(line) for line in f if line.strip()]
    
    master_set = set(master_genes)
    print(f"\nCluster {c}: {len(master_genes)} genes loaded.")

    for m in methods:
        # Index is the master list to keep the original order
        df = pd.DataFrame(0, index=master_genes, columns=runs)
        
        for r in runs:
            # Files are .txt in the subfolder
            pred_file = f"predictor_names_{c}_{m}_{r}.txt"
            pred_path = os.path.join(data_path, pred_file)

            if os.path.exists(pred_path):
                with open(pred_path, 'r') as f:
                    # Clean the file content and match
                    content = f.read().replace(',', ' ').split()
                    preds_in_file = [super_clean(w) for w in content if w.strip()]
                    
                    for p in preds_in_file:
                        if p in master_set:
                            df.at[p, r] = 1
            else:
                # Debug message to ensure we aren't missing files
                print(f"  Warning: Missing {pred_file}")
        
        # 2. Save
        output_name = f"reliability_cluster_{c}_method_{m}.csv"
        df.to_csv(os.path.join(base_path, output_name))
        print(f"  Method {m}: {df.values.sum()} matches found.")

print("\nProcessing complete.")
