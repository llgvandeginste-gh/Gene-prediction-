import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler

# 1. Load and Log Transform
df = pd.read_csv(r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\New_log2_cleaned_data.csv', index_col=0)
if df.shape[1] > df.shape[0]: df = df.T
 # df_log = np.log2(df + 1)

# 2. Prepare Data
# Scaling ensures the elbow reflects the Pearson-like relationship 
# by focusing on patterns rather than absolute magnitude.
scaled_data = StandardScaler().fit_transform(df)

# 3. Calculate WCSS
wcss = []
cluster_range = range(1, 11)
for i in cluster_range:
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42, n_init=10)
    kmeans.fit(scaled_data)
    wcss.append(kmeans.inertia_)

# 4. Find and Print Elbow
kn = KneeLocator(cluster_range, wcss, curve='convex', direction='decreasing')
optimal_k = kn.elbow
print("-" * 30)
print(f"The optimized number of clusters is: {optimal_k}")
print("-" * 30)

# 5. Generate the Elbow Plot
plt.figure(figsize=(10, 6))
plt.plot(cluster_range, wcss, marker='o', linestyle='--', color='b', label='WCSS (Inertia)')

# Add a vertical line and text to highlight the elbow
if optimal_k is not None:
    plt.axvline(x=optimal_k, color='r', linestyle=':', label=f'Elbow Point (K={optimal_k})')
    plt.annotate(f'Optimum K={optimal_k}', 
                 xy=(optimal_k, wcss[optimal_k-1]), 
                 xytext=(optimal_k+0.5, wcss[optimal_k-1]),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))

plt.title('Elbow Plot for Gene Expression Clustering')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
plt.xticks(cluster_range)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.show()