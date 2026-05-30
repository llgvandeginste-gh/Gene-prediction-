import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# 1. Load Data
df_expr = pd.read_csv('/Users/familievandeginste/Downloads/10_merged_174libs_0FPM.txt', sep='\t', index_col=0)

# Log2 Transform the whole matrix
df_log2 = np.log1p(df_expr) / np.log(2)

# Metrics list and letter labels for both figures
metrics = ['Mean', 'Median', 'Std', 'Min', 'Max', 'NA_Count']
letters = ['a', 'b', 'c', 'd', 'e', 'f']

# -----------------------------------------------------------------
# FIGURE 1: GENE STATS (RED)
# -----------------------------------------------------------------
stats_genes = pd.DataFrame({
    'Mean': df_log2.mean(axis=1),
    'Median': df_log2.median(axis=1),
    'Std': df_log2.std(axis=1),
    'Min': df_log2.min(axis=1),
    'Max': df_log2.max(axis=1),
    'NA_Count': df_log2.isna().sum(axis=1)
})

fig_genes, axes_genes = plt.subplots(1, 6, figsize=(25, 5))

for i, col in enumerate(metrics):
    data = stats_genes[col].dropna()
    
    if data.min() == data.max():
        bins = np.array([data.min() - 0.5, data.min() + 0.5])
    else:
        bins = np.linspace(data.min(), data.max(), 11)

    # Plot Gene Histogram (Red/Salmon)
    axes_genes[i].hist(data, bins=bins, color='salmon', alpha=0.4, edgecolor='black')
    
    # Plot Scaled KDE Line
    if len(data) > 1 and data.var() > 0:
        kde = gaussian_kde(data)
        x_range = np.linspace(bins.min(), bins.max(), 200)
        bin_width = (bins[1] - bins[0]) if isinstance(bins, np.ndarray) else 1
        scaled_kde = kde(x_range) * len(data) * bin_width
        axes_genes[i].plot(x_range, scaled_kde, color='salmon', lw=2.5)

    # Styling
    axes_genes[i].set_title(f'Genes Log2 {col}', fontsize=12, fontweight='bold', pad=12)
    axes_genes[i].set_xlabel(col, fontsize=11, labelpad=8)
    axes_genes[i].set_ylabel('Count', fontsize=11, labelpad=2)
    axes_genes[i].tick_params(axis='both', labelsize=10)
    axes_genes[i].grid(axis='y', linestyle='--', alpha=0.5)

# Force a physical spacing layout (wspace controls horizontal space between subplots)
fig_genes.subplots_adjust(left=0.05, right=0.98, top=0.85, bottom=0.2, wspace=0.4)

# Add letters safely underneath
for i, ax in enumerate(axes_genes):
    bbox = ax.get_position()
    fig_genes.text(bbox.x0, bbox.y0 - 0.1, letters[i], fontsize=16, fontweight='bold', verticalalignment='top', horizontalalignment='left')


# -----------------------------------------------------------------
# FIGURE 2: SAMPLE STATS (BLUE)
# -----------------------------------------------------------------
stats_samples = pd.DataFrame({
    'Mean': df_log2.mean(axis=0),
    'Median': df_log2.median(axis=0),
    'Std': df_log2.std(axis=0),
    'Min': df_log2.min(axis=0),
    'Max': df_log2.max(axis=0),
    'NA_Count': df_log2.isna().sum(axis=0)
})

fig_samples, axes_samples = plt.subplots(1, 6, figsize=(25, 5))

for i, col in enumerate(metrics):
    data = stats_samples[col].dropna()
    
    if data.min() == data.max():
        bins = np.array([data.min() - 0.5, data.min() + 0.5])
    else:
        bins = np.linspace(data.min(), data.max(), 11)

    # Plot Sample Histogram (Blue/Skyblue)
    axes_samples[i].hist(data, bins=bins, color='skyblue', alpha=0.4, edgecolor='black')
    
    # Plot Scaled KDE Line
    if len(data) > 1 and data.var() > 0:
        kde = gaussian_kde(data)
        x_range = np.linspace(bins.min(), bins.max(), 200)
        bin_width = (bins[1] - bins[0]) if isinstance(bins, np.ndarray) else 1
        scaled_kde = kde(x_range) * len(data) * bin_width
        axes_samples[i].plot(x_range, scaled_kde, color='skyblue', lw=2.5)

    # Styling
    axes_samples[i].set_title(f'Samples Log2 {col}', fontsize=12, fontweight='bold', pad=12)
    axes_samples[i].set_xlabel(col, fontsize=11, labelpad=8)
    axes_samples[i].set_ylabel('Count', fontsize=11, labelpad=8)
    axes_samples[i].tick_params(axis='both', labelsize=10)
    axes_samples[i].grid(axis='y', linestyle='--', alpha=0.5)

# Force a physical spacing layout
fig_samples.subplots_adjust(left=0.05, right=0.98, top=0.85, bottom=0.2, wspace=0.4)

# Add letters safely underneath
for i, ax in enumerate(axes_samples):
    bbox = ax.get_position()
    fig_samples.text(bbox.x0, bbox.y0 - 0.1, letters[i], fontsize=16, fontweight='bold', verticalalignment='top', horizontalalignment='left')

plt.show()