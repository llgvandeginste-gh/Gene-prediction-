import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_methods_from_file(df):
    # This helps you verify exactly what your columns are named
    #print("Detected columns in file:", df.columns.tolist())
    
    methods = [
        '0_index', 
        'a_variance_descending', 
        'b_pearsonr_descending', 
        'c_fewest_nonzero_predictors', 
        'd_random'
    ]
    
    for method in methods:
        # Filter for the specific method
        method_df = df[df['ordering_method'] == method]
        
        if method_df.empty:
            print(f"Skipping: No data found for method '{method}'")
            continue

        plt.figure(figsize=(10, 6))
        
        # Mapping:
        # x = n_preds_total
        # y = median_pearsonr_test
        # hue (color) = tolerance
        # size = gain_threshold
        # style (shape) = score_threshold
        sns.scatterplot(
            data=method_df,
            x='n_preds_total',
            y='median_pearsonr_test',
            hue='tolerance',
            size='gain_threshold',
            style='score_threshold',
            palette='viridis',
            sizes=(50, 300) 
        )

        plt.title(f"Ordering Method: {method}")
        plt.xlabel("Number of Predictors")
        plt.ylabel("Pearson r")
        
        # Moves the legend outside the plot so it doesn't cover the dots
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

# --- Load your data here ---
# Replace 'your_file.csv' with your actual filename
df = pd.read_csv(r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\cluster1_par50.csv') 
plot_methods_from_file(df)