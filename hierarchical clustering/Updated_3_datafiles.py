import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist

# 1. Data laden (reeds gelogd)
file_path = r'C:\Users\ilseh\OneDrive\Documenten\Python\New_log2_cleaned_data.csv'
df = pd.read_csv(file_path, index_col=0)

# Zorg dat genen in de RIJEN staan
if df.shape[1] > df.shape[0]: 
    df = df.T

# 2. Clustering (Pearson-Ward)
# We gebruiken de data direct voor de berekening
corr_dist = pdist(df, metric='correlation')
ward_pearson_dist = np.sqrt(2 * corr_dist)
Z = linkage(ward_pearson_dist, method='ward')

# 3. Clusters bepalen
num_clusters = 3
cluster_assignments = fcluster(Z, t=num_clusters, criterion='maxclust')

# 4. Opslaan per cluster ZONDER de extra kolom
print("-" * 40)
print("BESTANDEN OPSLAAN...")

for i in range(1, num_clusters + 1):
    # We zoeken de locaties (indexen) van de genen die bij cluster i horen
    gene_indices = (cluster_assignments == i)
    
    # We selecteren deze genen uit de originele dataframe
    # Hierdoor blijft de structuur exact hetzelfde als je bronbestand
    cluster_df = df.iloc[gene_indices]
    
    # Opslaan
    output_filename = f'new_log_gene_cluster_{i}_expression.csv'
    cluster_df.to_csv(output_filename)
    
    print(f"Cluster {i}: {len(cluster_df)} genen opgeslagen in {output_filename}")

print("-" * 40)
print("Klaar! De bestanden bevatten nu alleen de originele data.")