import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

input_dir = '/Users/familievandeginste/Documents/Pearsonr_tests/Final_model_parquet_all/Renamed_Results'
output_plots_dir = '/Users/familievandeginste/Documents/Pearsonr_tests/Density_Plots'

if not os.path.exists(output_plots_dir):
    os.makedirs(output_plots_dir)

clusters = ['1', '2', '3']
methods = ['0', 'a', 'b', 'c', 'd']
runs = range(1, 11)

print("Starting to generate density plots...")

for c in clusters:
    for m in methods:
        plt.figure(figsize=(10, 6))
        plot_title = f"Density of Pearson R - Cluster {c} - Method {m}"
        found_data = False
        
        # Overlay each of the 10 runs
        for r in runs:
            filename = f"final_model_results_{c}_{m}_{r}.parquet"
            file_path = os.path.join(input_dir, filename)
            
            if os.path.exists(file_path):
                # Load the parquet file
                df = pd.read_parquet(file_path)
                
                # Plot the density line for this specific run
                sns.kdeplot(df['pearsonr_test'], label=f"Run {r}", alpha=0.5, linewidth=1.5)
                found_data = True
            else:
                print(f"Warning: Missing file {filename}")
        
        if found_data:
            plt.title(plot_title, fontsize=14)
            plt.xlabel("Pearson R (Training Set)", fontsize=12)
            plt.ylabel("Density", fontsize=12)
            plt.xlim(-0.1, 1.1)  # Provides a bit of breathing room for the curves
            plt.grid(axis='y', linestyle='--', alpha=0.3)
            plt.legend(title="Runs", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            
            # Save the plot
            save_path = os.path.join(output_plots_dir, f"density_c{c}_m{m}.png")
            plt.savefig(save_path, dpi=300) # High resolution for your report
            print(f"Successfully saved: {save_path}")
        
        plt.close() 

print(f"\nDone! All 15 plots are in: {output_plots_dir}")


total_files_found = 0
for c in clusters:
    for m in methods:
        for r in runs:
            if os.path.exists(os.path.join(input_dir, f"final_model_results_{c}_{m}_{r}.parquet")):
                total_files_found += 1

print(f"VERIFICATION: Found {total_files_found} out of 150 expected files.")
