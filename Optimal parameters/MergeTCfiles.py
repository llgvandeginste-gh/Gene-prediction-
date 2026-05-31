import pandas as pd
import glob
import os

# 1. Define the path where your average_tc_results_X.csv files are stored
# The '*' is a wildcard that will find _1, _2, _3, etc.
path = '/Users/familievandeginste/Documents/100par_matrix/average_tc_results_*.csv'
all_files = glob.glob(path)

merged_list = []

# 2. Loop through each file found
for filename in all_files:
    # Read the file
    df = pd.read_csv(filename)
    
    # Extract the cluster number from the filename
    # Example: 'average_tc_results_1.csv' -> split by '_' -> get index 3 -> remove '.csv'
    base_name = os.path.basename(filename)
    cluster_num = base_name.split('_')[-1].replace('.csv', '')
    
    # Add the cluster column to this dataframe
    df['cluster'] = cluster_num
    
    merged_list.append(df)

# 3. Concatenate all clusters into one big DataFrame
df_all_clusters = pd.concat(merged_list, ignore_index=True)

# 4. Save the final merged file
output_path = '/Users/familievandeginste/Documents/100par_matrix/all_clusters_average_TC_merged.csv'
df_all_clusters.to_csv(output_path, index=False)

print(f"Successfully merged {len(all_files)} cluster files into one master list.")
print(df_all_clusters.head())