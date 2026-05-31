import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# File paths
metadata_file = r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\10_merged_174libs_samples.txt'
expression_file = r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\10_merged_174libs_0FPM.txt'
geslacht_kolom = 'Sex'  
man_label = 'M'            
vrouw_label = 'F'       

# Load data
metadata = pd.read_csv(metadata_file, sep='\t', index_col=0)
expression = pd.read_csv(expression_file, sep='\t', index_col=0)

# Log transformation
expression_log = np.log2(expression + 1)

# Split sample IDs by group
ids_man = metadata[metadata[geslacht_kolom] == man_label].index
ids_vrouw = metadata[metadata[geslacht_kolom] == vrouw_label].index

# Calculate summary statistics ACROSS GENES (axis=0) per sample
stats_man = pd.DataFrame(index=ids_man)
stats_man['Mean']   = expression_log[ids_man].mean(axis=0)
stats_man['Median'] = expression_log[ids_man].median(axis=0)
stats_man['SD']     = expression_log[ids_man].std(axis=0)
stats_man['Min']    = expression_log[ids_man].min(axis=0)
stats_man['Max']    = expression_log[ids_man].max(axis=0)
stats_man['Group']  = man_label

stats_vrouw = pd.DataFrame(index=ids_vrouw)
stats_vrouw['Mean']   = expression_log[ids_vrouw].mean(axis=0)
stats_vrouw['Median'] = expression_log[ids_vrouw].median(axis=0)
stats_vrouw['SD']     = expression_log[ids_vrouw].std(axis=0)
stats_vrouw['Min']    = expression_log[ids_vrouw].min(axis=0)
stats_vrouw['Max']    = expression_log[ids_vrouw].max(axis=0)
stats_vrouw['Group']  = vrouw_label

# Combine the dataframes
combined_full = pd.concat([stats_man, stats_vrouw])

# Plotting
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle(f'Comparison sample statistics: {man_label} vs. {vrouw_label}', fontsize=20, y=0.98)

metrics = ['Mean', 'Median', 'SD', 'Min', 'Max']
palette_colors = {man_label: "skyblue", vrouw_label: "salmon"}

for i, metric in enumerate(metrics):
    row = i // 3
    col = i % 3
    ax = axes[row, col]
    
    # --- FIX: Only use KDE if the metric actually has variance ---
    # Min and Max often have identical values across all samples, crashing the KDE math.
    use_kde = False if metric in ['Min', 'Max'] else True
    
    sns.histplot(data=combined_full, x=metric, hue='Group', 
                 kde=use_kde, ax=ax, palette=palette_colors, 
                 element="step", common_norm=False, bins=15)
    
    ax.set_title(f'Distribution of Sample {metric}', fontsize=14)
    ax.set_xlabel(f'{metric} Value (per sample)')
    ax.set_ylabel('Number of samples')

# Remove the empty subplot
fig.delaxes(axes[1, 2])

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()