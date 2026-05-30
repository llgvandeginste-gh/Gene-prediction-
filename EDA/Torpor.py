import pandas as pd

df_expr = pd.read_csv('/Users/familievandeginste/Downloads/10_merged_174libs_0FPM.txt', sep='\t', index_col=0)
df_meta = pd.read_csv('/Users/familievandeginste/Documents/EDA/10_merged_174libs_samples.txt', sep = '\t', index_col=0)

df_expr = df_expr[df_meta.index]
print(df_meta['Group'].unique())

subsets = {}
stages = df_meta['Group'].unique()


sample_ids_TL = df_meta[df_meta['Group'] == 'TL'].index
    
subsets['TL'] = df_expr[sample_ids_TL]

df_torpor_late = subsets['TL']
df_torpor_late.to_csv('Torpor_late_summary.csv', index=False)

sample_ids_TE = df_meta[df_meta['Group'] == 'TE'].index
    
subsets['TE'] = df_expr[sample_ids_TE]

df_torpor_early = subsets['TE']
df_torpor_early.to_csv('Torpor_early_summary.csv', index=False)

sample_ids_AL = df_meta[df_meta['Group'] == 'AL'].index

subsets['AL'] = df_expr[sample_ids_AL]

df_active_late = subsets['AL']
df_active_late.to_csv('Active_late_summary.csv', index=False)

sample_ids_AE = df_meta[df_meta['Group'] == 'AE'].index
    
subsets['AE'] = df_expr[sample_ids_AE]

df_active_early = subsets['AE']
df_active_early.to_csv('Active_early_summary.csv', index=False)

sample_ids_SE = df_meta[df_meta['Group'] == 'SE'].index
    
subsets['SE'] = df_expr[sample_ids_SE]

df_summer_euthermia = subsets['SE']
df_summer_euthermia.to_csv('Summer_euthermia_summary.csv', index=False)

print(df_torpor_late.head())
print(df_torpor_early.head())
print(df_active_late.head())
print(df_active_early.head())
print(df_summer_euthermia.head())

import numpy as np
# df_log = np.log1p(df)

# df_log2_torpor_late = np.log1p(df_torpor_late) / np.log(2)

# Sample_stats_df_torpor_late = df_torpor_late.agg(['mean', 'median', 'std', 'min', 'max', lambda x: x.isna().sum()]).T

# Sample_stats_df_torpor_late.columns = ['Mean', 'Median', 'Std', 'Min', 'Max', 'NA_Count']
# Sample_stats_df_torpor_late.index.name = 'Gene_ID'

# Gene_stats_df_torpor_late = pd.DataFrame({
#     'Mean': df_log2_torpor_late.mean(axis=1),
#     'Median': df_log2_torpor_late.median(axis=1),
#     'Std': df_log2_torpor_late.std(axis=1),
#     'Min': df_log2_torpor_late.min(axis=1),
#     'Max': df_log2_torpor_late.max(axis=1),
#     'NA_Count': df_log2_torpor_late.isna().sum(axis=1)
# })

# import matplotlib.pyplot as plt
# import seaborn as sns

# fig, axes = plt.subplots(1, 6, figsize=(20, 4))
# metrics = ['Mean', 'Median', 'Std', 'Min', 'Max', 'NA_Count']

# for i, col in enumerate(metrics):
#     sns.histplot(Sample_stats_df_torpor_late[col], kde=True, ax=axes[i], color='skyblue')
#     axes[i].set_title(f'Sample {col}')

# plt.tight_layout()
# plt.show()

# fig, axes = plt.subplots(1, 6, figsize=(20, 4))

# for i, col in enumerate(metrics):
#     sns.histplot(Gene_stats_df_torpor_late[col], kde=True, ax=axes[i], color='salmon')
#     axes[i].set_title(f'Gene {col}')

# plt.tight_layout()
# plt.show()

# df_torpor_late.shape

# df_log2_SE = np.log1p(df_summer_euthermia) / np.log(2)

# Sample_stats_df_SE = df_summer_euthermia.agg(['mean', 'median', 'std', 'min', 'max', lambda x: x.isna().sum()]).T

# Sample_stats_df_SE.columns = ['Mean', 'Median', 'Std', 'Min', 'Max', 'NA_Count']
# Sample_stats_df_SE.index.name = 'Gene_ID'

# Gene_stats_df_SE = pd.DataFrame({
#     'Mean': df_log2_SE.mean(axis=1),
#     'Median': df_log2_SE.median(axis=1),
#     'Std': df_log2_SE.std(axis=1),
#     'Min': df_log2_SE.min(axis=1),
#     'Max': df_log2_SE.max(axis=1),
#     'NA_Count': df_log2_SE.isna().sum(axis=1)
# })

# import matplotlib.pyplot as plt
# import seaborn as sns

# fig, axes = plt.subplots(1, 6, figsize=(20, 4))
# metrics = ['Mean', 'Median', 'Std', 'Min', 'Max', 'NA_Count']

# for i, col in enumerate(metrics):
#     sns.histplot(Sample_stats_df_SE[col], kde=True, ax=axes[i], color='skyblue')
#     axes[i].set_title(f'Sample {col}')

# plt.tight_layout()
# plt.show()

# fig, axes = plt.subplots(1, 6, figsize=(20, 4))

# for i, col in enumerate(metrics):
#     sns.histplot(Gene_stats_df_SE[col], kde=True, ax=axes[i], color='salmon')
#     axes[i].set_title(f'Gene {col}')

# plt.tight_layout()
# plt.show()

# df_summer_euthermia.shape

top_genes_TE = df_torpor_early.mean(axis=1).sort_values(ascending=False).head(20)

print("Top 20 most expressed genes TE:")
print(top_genes_TE)

top_genes_TL = df_torpor_late.mean(axis=1).sort_values(ascending=False).head(20)

print("Top 20 most expressed genes across TL:")
print(top_genes_TL)

top_genes_AE = df_active_early.mean(axis=1).sort_values(ascending=False).head(20)

print("Top 20 most expressed genes across AE:")
print(top_genes_AE)

top_genes_AL = df_active_late.mean(axis=1).sort_values(ascending=False).head(20)

print("Top 20 most expressed genes across AL:")
print(top_genes_AL)

top_genes_SE = df_summer_euthermia.mean(axis=1).sort_values(ascending=False).head(20)

print("Top 20 most expressed genes across SE:")
print(top_genes_SE)

co_expressors = df_expr.corrwith(df_expr.loc['Equ03.20845'], axis=1)
# Assuming your correlation series is called 'co_expressors'
# Sort them to find the strongest matches
top_partners = co_expressors.sort_values(ascending=False).head(15)

print("The Target's Closest Allies (Strongest Positive Correlation):")
print(top_partners)