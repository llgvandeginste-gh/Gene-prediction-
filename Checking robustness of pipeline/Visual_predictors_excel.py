import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


file_map = {
   r'C:\Users\ilseh\Downloads\reliability_cluster_3_method_0.csv': 'Method_0',
    r'C:\Users\ilseh\Downloads\reliability_cluster_3_method_a.csv': 'Method_a',
    r'C:\Users\ilseh\Downloads\reliability_cluster_3_method_b.csv': 'Method_b',
    r'C:\Users\ilseh\Downloads\reliability_cluster_3_method_c.csv': 'Method_c',
    r'C:\Users\ilseh\Downloads\reliability_cluster_3_method_d.csv': 'Method_d'
}

def analyze_and_export(mapping, output_excel='Gene_Analysis_Results.xlsx'):
    
    sns.set_theme(style="whitegrid")
    num_methods = len(mapping)
    fig, axes = plt.subplots(1, num_methods, figsize=(4 * num_methods, 5), sharey=True)
    
    if num_methods == 1: axes = [axes]

   
    all_method_counts = []

    for i, (file_path, clean_name) in enumerate(mapping.items()):
        if not os.path.exists(file_path):
            print(f"Skipping {file_path}: File not found.")
            continue
            
        # Load the matrix
        df = pd.read_csv(file_path, index_col=0)
        row_sums = df.sum(axis=1).astype(int)
        
        # Visualization Section 
        sns.histplot(row_sums, bins=12, kde=True, ax=axes[i], color='teal', edgecolor='white')
        axes[i].set_title(clean_name, fontweight='bold', fontsize=14, pad=20)
        axes[i].set_xlabel('Times Selected')
        if i == 0: axes[i].set_ylabel('Number of Genes')
        
        # Table Data Section 
        # Get counts for every sum (how many genes selected 0, 1, 2... times)
        counts = row_sums.value_counts().sort_index().reset_index()
        counts.columns = ['Selection Count', 'Gene Count']
        counts['Method'] = clean_name
        all_method_counts.append(counts)

    # Save the plots
    plt.tight_layout()
    plt.savefig('gene_predictor_plots.png', dpi=300)
    plt.show()

    # Excel Export Section 
    if all_method_counts:
        # Combine data and pivot so Methods are columns
        combined_df = pd.concat(all_method_counts)
        pivot_table = combined_df.pivot(index='Selection Count', columns='Method', values='Gene Count')
        
        # Fill missing values (cases where a count was never reached) with 0
        pivot_table = pivot_table.fillna(0).astype(int)
        
        # Save to Excel
        pivot_table.to_excel(output_excel)
        print(f"Success! Frequency table saved to: {output_excel}")
        return pivot_table
    else:
        print("No data found to save to Excel.")
        return None

# Run the analysis
if __name__ == "__main__":
    final_table = analyze_and_export(file_map)
