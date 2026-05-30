import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist

# 1. Load Data
file_path = r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\New_log2_cleaned_data.csv'
df = pd.read_csv(file_path, index_col=0)

# Ensure Genes are ROWS (Standard for Gene Expression Heatmaps)
if df.shape[1] > df.shape[0]:
    df = df.T

# --- 2. GENE CLUSTERING (Rows) ---
# Calculate Pearson Distance for Genes
gene_corr_dist = pdist(df, metric='correlation')
gene_ward_dist = np.sqrt(2 * gene_corr_dist)
Z_genes = linkage(gene_ward_dist, method='ward')

# Extract 3 Gene Clusters
gene_clusters = fcluster(Z_genes, t=3, criterion='maxclust')

# --- 3. SAMPLE CLUSTERING (Columns) ---
# Calculate Pearson Distance for Samples (we transpose df to get columns)
sample_corr_dist = pdist(df.T, metric='correlation')
sample_ward_dist = np.sqrt(2 * sample_corr_dist)
Z_samples = linkage(sample_ward_dist, method='ward')

# --- 4. TERMINAL OUTPUT ---
print("-" * 30)
print("GENE CLUSTER COUNTS (ROWS)")
print(pd.Series(gene_clusters, index=df.index).value_counts().sort_index())
print("-" * 30)

# --- 5. VISUALIZATION ---
# We now pass both row_linkage and col_linkage to sns.clustermap
g = sns.clustermap(df, 
                   row_linkage=Z_genes, 
                   col_linkage=Z_samples, 
                   cmap='RdBu_r', 
                   #z_score=0,      # Normalize genes (rows), remove # when wanting to see expression regarding the mean gene expression
                   #center=0,       # add # when wanting to know the absolute values of expression
                   figsize=(12, 10))

# Adding titles and labels
g.fig.suptitle('Bi-Clustered Heatmap (Ward-Pearson Distance)', y=1.02)
plt.show()