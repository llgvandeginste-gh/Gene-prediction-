import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_single_file(file_path):
    # 1. Load the single data file
    df = pd.read_csv(file_path)
    
    # Define the 5 methods to plot
    methods = [
        '0_index', 
        'a_variance_descending', 
        'b_pearsonr_descending', 
        'c_fewest_nonzero_predictors', 
        'd_random'
    ]
    
    # 2. Create the 1x5 grid
    # sharey=True ensures the Pearson r scale is identical for comparison
    fig, axes = plt.subplots(1, 5, figsize=(28, 7), sharey=True)
    
    for i, method in enumerate(methods):
        ax = axes[i]
        method_df = df[df['ordering_method'] == method]
        
        if method_df.empty:
            ax.set_title(f"{method}\n(No Data)")
            continue

        sns.scatterplot(
            data=method_df,
            x='n_preds_total',
            y='median_pearsonr_test',
            hue='tolerance',
            size='gain_threshold',
            style='score_threshold', 
            palette='viridis',
            sizes=(40, 240),
            ax=ax,
            legend=(i == 4)  # Show legend only on the last plot to prevent clutter
        )

        ax.set_title(method, fontsize=12, fontweight='bold')
        ax.set_xlabel("N Predictors")
        
        # Only label the y-axis on the first plot
        if i == 0:
            ax.set_ylabel("Pearson r")
        
        ax.grid(True, linestyle='--', alpha=0.4)

    # Place legend outside the plots on the right
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Parameters")
    
    plt.suptitle("Analysis: Parameter Effect on Gene Prediction", fontsize=16, y=1.02)
    plt.tight_layout()
    plt.show()

# --- Execution ---
# Replace with your actual file name
plot_single_file(r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\cluster3_100par.csv')