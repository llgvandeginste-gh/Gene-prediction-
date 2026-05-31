import pandas as pd

# 1. Load your average TC results
df_avg = pd.read_csv('/Users/familievandeginste/Documents/100par_matrix/average_tc_results_3.csv')

# 2. Define a dictionary to map short labels to the long names in your big matrix
method_map = {
    '0': '0_index',
    'a': 'a_variance_descending',
    'b': 'b_pearsonr_descending',
    'c': 'c_fewest_nonzero_predictors',
    'd': 'd_random'
}

# 3. Extract parameters from the name string
def parse_params(name):
    try:
        parts = str(name).split('_')
        # Get the short label (0, a, b, c, or d)
        short_method = parts[1] 
        
        # Convert short label to the long name used in the big matrix
        long_method = method_map.get(short_method, short_method)
        
        tol = [p.replace('tol', '') for p in parts if 'tol' in p][0]
        gain = [p.replace('gain', '') for p in parts if 'gain' in p][0]
        score = [p.replace('score', '') for p in parts if 'score' in p][0]
        
        return pd.Series([long_method, float(tol), float(gain), float(score)])
    except (IndexError, ValueError, TypeError):
        return pd.Series([None, None, None, None])

# 4. Apply parsing and set column names
new_cols = df_avg['Parameter_Combination'].apply(parse_params)
new_cols.columns = ['ordering_method', 'tolerance', 'gain_threshold', 'score_threshold']
df_avg = pd.concat([df_avg, new_cols], axis=1)
df_avg = df_avg.dropna(subset=['ordering_method'])

# 5. Load your big pipeline metrics file
df_grid = pd.read_csv('/Users/familievandeginste/Documents/100par_matrix/cluster3_100par.csv')

# 6. Ensure all merge keys are the same type
for col in ['ordering_method', 'tolerance', 'gain_threshold', 'score_threshold']:
    df_avg[col] = df_avg[col].astype(str)
    df_grid[col] = df_grid[col].astype(str)

# 7. Merge
df_combined = df_grid.merge(
    df_avg[['ordering_method', 'tolerance', 'gain_threshold', 'score_threshold', 'Average_TC']], 
    on=['ordering_method', 'tolerance', 'gain_threshold', 'score_threshold'], 
    how='left'
)

# 8. Save
output_path = '/Users/familievandeginste/Documents/100par_matrix/grid_with_TC_metrics_3.csv'
df_combined.to_csv(output_path, index=False)

# Check if it worked
filled_rows = df_combined['Average_TC'].notna().sum()
print(f"Success! Found matches for {filled_rows} rows.")