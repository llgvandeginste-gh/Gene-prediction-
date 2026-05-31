import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load your cluster matrix
# Ensure index_col=0 so the gene names are the index, not a column
df = pd.read_csv('matrix_cluster_1_all_methods.csv', index_col=0)

# Count exactly how many rows sum to zero
zeros = (df.sum(axis=1) == 0).sum()
print(f"Genes mentioned zero times: {zeros}")

# 2. Calculate the selection frequency for each gene
# axis=1 sums horizontally (across all method/parameter columns)
gene_frequencies = df.sum(axis=1)

# 3. Create the Histogram
plt.figure(figsize=(10, 6))
sns.histplot(gene_frequencies, bins=30, kde=False, color='skyblue', edgecolor='black')

# Formatting
plt.title('General Gene Selection Frequency - Cluster 1')
plt.xlabel('Number of Times Selected (Across all Parameters/Methods)')
plt.ylabel('Number of Genes')
plt.grid(axis='y', alpha=0.3)

plt.show()