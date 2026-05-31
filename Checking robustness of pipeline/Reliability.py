import pandas as pd
import numpy as np
import os

folder_path = r'/Users/familievandeginste/Documents/Predictors_responders'
methods = ['0', 'a', 'b', 'c', 'd']
clusters = [1, 2, 3]

def calculate_jaccard(df):
    """Calculates the average Jaccard Index between all pairs of runs."""
    cols = df.columns
    jaccards = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            set_i = set(df.index[df[cols[i]] == 1])
            set_j = set(df.index[df[cols[j]] == 1])
            if not set_i and not set_j: continue
            
            intersection = len(set_i.intersection(set_j))
            union = len(set_i.union(set_j))
            jaccards.append(intersection / union)
    return np.mean(jaccards) if jaccards else 0

print(f"{'Method':<10} | {'Cluster':<10} | {'Avg Genes/Run':<15} | {'Stability (Jaccard)':<20}")
print("-" * 65)

for c in clusters:
    for m in methods:
        file_name = f"reliability_cluster_{c}_method_{m}.csv"
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.exists(file_path):
            # Load table (index is the gene names)
            df = pd.read_csv(file_path, index_col=0)
            
            # 1. Average genes selected per run
            avg_genes = df.sum(axis=0).mean()
            
            # 2. Jaccard Stability
            stability = calculate_jaccard(df)
            
            # 3. Frequency - identify "Top Reliable Genes"
            # (Genes selected in > 80% of runs)
            df['Frequency'] = df.sum(axis=1) / 10
            top_genes_count = len(df[df['Frequency'] >= 0.8])
            
            print(f"{m:<10} | {c:<10} | {avg_genes:<15.1f} | {stability:<20.3f}")

print("\nAnalysis complete.")


summary_data = []

for c in clusters:
    for m in methods:
        file_path = os.path.join(folder_path, f"reliability_cluster_{c}_method_{m}.csv")
        if os.path.exists(file_path):
            temp_df = pd.read_csv(file_path, index_col=0)
            
            # Calculate consistency per gene
            # Frequency of selection (e.g., 0.9 means selected in 9/10 runs)
            selection_freq = temp_df.sum(axis=1) / 10
            
            avg_genes = temp_df.sum(axis=0).mean()
            stability = calculate_jaccard(temp_df)
            
            # Statistics for Selection Probability
            # Percentage of the total gene pool that was selected in EVERY run
            prob_100 = (selection_freq == 1.0).sum()
            # Percentage of the total gene pool selected in at least 80% of runs
            prob_80 = (selection_freq >= 0.8).sum()

            summary_data.append({
                'Method': m,
                'Cluster': c,
                'Avg_Genes_Per_Run': round(avg_genes, 2),
                'Stability_Jaccard': round(stability, 3),
                'Stable_Genes_100pct': int(prob_100),
                'Stable_Genes_80pct': int(prob_80)
            })

# Create and save
summary_df = pd.DataFrame(summary_data)
summary_output_path = os.path.join(folder_path, "pipeline_stability_summary.csv")

# Save with European formatting
summary_df.to_csv(summary_output_path, index=False, sep=';', decimal=',')

print(f"\nSummary table with Selection Probability saved to: {summary_output_path}")
