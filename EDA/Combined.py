import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde

# 1. Load Data
df_expr = pd.read_csv('/Users/familievandeginste/Downloads/10_merged_174libs_0FPM.txt', sep='\t', index_col=0)
df_meta = pd.read_csv('/Users/familievandeginste/Documents/EDA/10_merged_174libs_samples.txt', sep='\t', index_col=0)
df_expr = df_expr[df_meta.index]

# 2. Subset and Log2 Transform
brain_ids = df_meta[df_meta['Tissue'].isin(['Cereb', 'Cortex', 'Hippoc', 'Hypoth'])].index
periph_ids = df_meta[df_meta['Tissue'].isin(['Kidney', 'Liver', 'BAT', 'WAT'])].index

df_log2_brain = np.log1p(df_expr[brain_ids]) / np.log(2)
df_log2_periph = np.log1p(df_expr[periph_ids]) / np.log(2)

# 3. Calculate Stats (Removed 'Min' and 'NA_Count')
metrics = ['Mean', 'Median', 'Std', 'Max']
letters = ['a', 'b', 'c', 'd']

stats_brain = df_log2_brain.agg(['mean', 'median', 'std', 'max']).T
stats_periph = df_log2_periph.agg(['mean', 'median', 'std', 'max']).T
stats_brain.columns = stats_periph.columns = metrics

# Adjust to 1 row, 4 columns
fig, axes = plt.subplots(1, 4, figsize=(18, 5))

for i, col in enumerate(metrics):
    b_data = stats_brain[col].dropna()
    p_data = stats_periph[col].dropna()
    combined = pd.concat([b_data, p_data])
    
    if combined.min() == combined.max():
        bins = 1
    else:
        bins = np.linspace(combined.min(), combined.max(), 11)

    # Plot both Brain and Periphery
    for data, color, label in [(b_data, 'skyblue', 'Brain'), (p_data, 'salmon', 'Periphery')]:
        axes[i].hist(data, bins=bins, color=color, alpha=0.4, 
                     label=label, edgecolor='black')
        
        # Plot Scaled KDE Line
        if len(data) > 1 and data.var() > 0:
            kde = gaussian_kde(data)
            x_range = np.linspace(bins.min(), bins.max(), 200)
            bin_width = (bins[1] - bins[0]) if isinstance(bins, np.ndarray) else 1
            scaled_kde = kde(x_range) * len(data) * bin_width
            axes[i].plot(x_range, scaled_kde, color=color, lw=2.5)

    # Styling and Readability
    axes[i].set_title(f'Sample {col}', fontsize=14, fontweight='bold', pad=12)
    axes[i].set_xlabel(f'Log2 Expression {col}', fontsize=12, labelpad=8)
    axes[i].set_ylabel('Sample Count', fontsize=12, labelpad=8)
    axes[i].tick_params(axis='both', labelsize=11)
    axes[i].grid(axis='y', linestyle='--', alpha=0.5)

    # Add legend to all plots cleanly or just the first one
    if i == 0: 
        axes[i].legend(fontsize=11, loc='upper right')

# Use tight_layout first so subplots are fixed in their final positions
plt.tight_layout()

# 4. Add the letters underneath the bottom-left corner of each graph
# We read the position of each axis and place the text slightly below it
for i, ax in enumerate(axes):
    bbox = ax.get_position()
    # bbox.x0 is the left edge of the subplot, bbox.y0 is the bottom edge
    fig.text(bbox.x0, bbox.y0 - 0.06, letters[i], 
             fontsize=16, 
             fontweight='bold', 
             verticalalignment='top', 
             horizontalalignment='left')

plt.show()

# # GRAPHS APART FROM EACHOTHER ON SAME AXES
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns


# # 1. Load Data

# df_expr = pd.read_csv('/Users/familievandeginste/Downloads/10_merged_174libs_0FPM.txt', sep='\t', index_col=0)
# df_meta = pd.read_csv('/Users/familievandeginste/Documents/EDA/10_merged_174libs_samples.txt', sep='\t', index_col=0)
# df_expr = df_expr[df_meta.index]

# # 2. Subset and Log2 Transform

# brain_ids = df_meta[df_meta['Tissue'].isin(['Cereb', 'Cortex', 'Hippoc', 'Hypoth'])].index
# periph_ids = df_meta[df_meta['Tissue'].isin(['Kidney', 'Liver', 'BAT', 'WAT'])].index

# df_log2_brain = np.log1p(df_expr[brain_ids]) / np.log(2)
# df_log2_periph = np.log1p(df_expr[periph_ids]) / np.log(2)

# # 3. Calculate Stats
# metrics = ['Mean', 'Median', 'Std', 'Min', 'Max', 'NA_Count']
# stats_brain = df_log2_brain.agg(['mean', 'median', 'std', 'min', 'max', lambda x: x.isna().sum()]).T
# stats_periph = df_log2_periph.agg(['mean', 'median', 'std', 'min', 'max', lambda x: x.isna().sum()]).T
# stats_brain.columns = stats_periph.columns = metrics

# # 4. Plotting: 2 rows, 6 columns
# fig, axes = plt.subplots(2, 6, figsize=(24, 8), sharex='col')

# for i, col in enumerate(metrics):
#     # 1. Combine data to find the global range (min to max)
#     # We use this to make sure the bins are IDENTICAL for both graphs
#     combined = pd.concat([stats_brain[col], stats_periph[col]]).dropna()
    
#     # 2. Define the bins manually. 
#     # 50 bins makes them thin. Use 100 if you want them even thinner.
#     # We use a safety check: if min == max, we just use 1 bin.
#     if combined.min() == combined.max():
#         bins = 1
#     else:
#         bins = np.linspace(combined.min(), combined.max(), 11)

#     # 3. Plot Brain (Top Row)
#     # 'edgecolor=None' makes the bars touch (no gaps)
#     axes[0, i].hist(stats_brain[col].dropna(), bins=bins, 
#                     color='skyblue', alpha=0.7, edgecolor = 'black')
#     axes[0, i].set_title(f'Brain {col}')
    
#     # 4. Plot Periphery (Bottom Row)
#     # Using the exact same 'bins' variable ensures they are the same size
#     axes[1, i].hist(stats_periph[col].dropna(), bins=bins, 
#                     color='salmon', alpha=0.7, edgecolor='black')
#     axes[1, i].set_title(f'Periphery {col}')

# plt.tight_layout()
# plt.show()

# import seaborn as sns
# import matplotlib.pyplot as plt

# # Create a clean dataframe for plotting
# data = pd.DataFrame({
#     'Median': pd.concat([stats_brain['Median'], stats_periph['Median']]),
#     'Group': ['Brain']*len(stats_brain) + ['Periphery']*len(stats_periph)
# })

# plt.figure(figsize=(6, 8))

# # Stripplot shows every single data point as a dot
# # jitter=True spreads them out horizontally so you can see overlapping points
# sns.stripplot(data=data, x='Group', y='Median', hue='Group', 
#               palette=['skyblue', 'salmon'], jitter=0.2, size=5, alpha=0.7)

# plt.title('Literal Sample Medians')
# plt.grid(axis='y', linestyle='--', alpha=0.5) # Adds lines to help read the values
# plt.show()

# # To see the actual numbers in the console:
# print("Brain Medians:\n", stats_brain['Median'].values)
# print("\nPeriphery Medians:\n", stats_periph['Median'].values)