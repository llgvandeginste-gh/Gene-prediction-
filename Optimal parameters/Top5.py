import pandas as pd

# 1. Read the file
df = pd.read_csv('combined_clusters_100par.csv')

# 2. Define your columns
pearson_col = 'median_pearsonr_test'
cluster_col = 'cluster'
method_col = 'ordering_method'

# 3. Extract Top 5 per Method per Cluster
# We sort everything first, then group by both Cluster and Method
df_top25 = (
    df.sort_values([cluster_col, method_col, pearson_col], ascending=[True, True, False])
    .groupby([cluster_col, method_col])
    .head(5)
    .reset_index(drop=True)
)

# 4. Save the result
df_top25.to_csv('top_5_pearson_combined.csv', index=False)

# 5. Quick Verification
total_rows = len(df_top25)
clusters = df_top25[cluster_col].nunique()
print(f"Extraction complete! Total rows: {total_rows}")
print(f"Calculated: {clusters} clusters * 5 methods * 5 results = {clusters * 25} expected rows.")
import pandas as pd

# 1. Load the files
df_top5 = pd.read_csv('top_5_pearson_combined.csv')
df_tc = pd.read_csv('all_clusters_average_TC_merged.csv')

# 2. Extract shorthand method from the TC file's 'Parameter_Combination'
# Example: 'method_a_0.001tol...' -> 'a'
df_tc['method_short'] = df_tc['Parameter_Combination'].str.split('_').str[1]

# 3. Extract shorthand method from the Top 5 'ordering_method'
# Example: 'a_variance_descending' -> 'a'
df_top5['method_short'] = df_top5['ordering_method'].str.split('_').str[0]

# 4. Standardize 'cluster' as integers in both to avoid merge errors
df_top5['cluster'] = df_top5['cluster'].astype(int)
df_tc['cluster'] = df_tc['cluster'].astype(int)

# 5. Extract thresholds from the TC file to match Top 5 column names
def parse_tc_params(name):
    parts = str(name).split('_')
    tol = [p.replace('tol', '') for p in parts if 'tol' in p][0]
    gain = [p.replace('gain', '') for p in parts if 'gain' in p][0]
    score = [p.replace('score', '') for p in parts if 'score' in p][0]
    return pd.Series([float(tol), float(gain), float(score)])

df_tc[['tolerance', 'gain_threshold', 'score_threshold']] = df_tc['Parameter_Combination'].apply(parse_tc_params)

# 6. Merge! 
# We match on cluster, method shorthand, and all three thresholds
df_final = df_top5.merge(
    df_tc[['cluster', 'method_short', 'tolerance', 'gain_threshold', 'score_threshold', 'Average_TC']],
    on=['cluster', 'method_short', 'tolerance', 'gain_threshold', 'score_threshold'],
    how='left'
)

# 7. Cleanup and Save
df_final = df_final.drop(columns=['method_short']) # Remove the temporary shorthand column
df_final.to_csv('top_5_with_average_TC.csv', index=False)

print("Success! 'Average_TC' column added to your Top 5 results.")
print(df_final[['cluster', 'ordering_method', 'median_pearsonr_test', 'Average_TC']].head())