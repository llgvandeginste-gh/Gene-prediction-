import pandas as pd
import numpy as np

# 1. Load the matrix you just created
file_path = '/Users/familievandeginste/Documents/100par_matrix/matrix_with_TC.csv'
df = pd.read_csv(file_path)

# 2. Identify all the parameter (method) columns
# We assume they all start with 'method_'
method_cols = [col for col in df.columns if col.startswith('method_')]

# 3. Ensure TC is a number (if there are NaNs from the merge, we fill them with 0)
df['TC'] = pd.to_numeric(df['TC'], errors='coerce').fillna(0)

# 4. Calculate the average TC for each column
# We multiply the column (0 or 1) by the TC value, then divide by the sum of 1s
results = {}

for col in method_cols:
    # Get only the rows where this specific gene was a predictor (value == 1)
    tc_values_for_predictors = df.loc[df[col] == 1, 'TC']
    
    # Calculate the average for this column
    if len(tc_values_for_predictors) > 0:
        results[col] = tc_values_for_predictors.mean()
    else:
        results[col] = 0  # In case a column has no predictors at all

# 5. Convert results to a new DataFrame
df_averages = pd.DataFrame(list(results.items()), columns=['Parameter_Combination', 'Average_TC'])

# 6. Save the results to a new file
output_path = '/Users/familievandeginste/Documents/100par_matrix/average_tc_results.csv'
df_averages.to_csv(output_path, index=False)

print(f"Success! Averages calculated for {len(method_cols)} columns.")
print(df_averages.head())

import pandas as pd

# 1. Load the file
df = pd.read_csv('/Users/familievandeginste/Documents/100par_matrix/matrix_with_TC.csv')

# 2. Pick the first method column to check
test_col = [c for c in df.columns if 'method_' in c][0]

# 3. Filter rows where this method has a 1
predictors = df[df[test_col] == 1]

# 4. Get the TC values for these specific rows
tc_values = predictors['TC'].dropna() # Remove NaNs so they don't skew the count

# 5. Calculate manually
sum_tc = tc_values.sum()
count_tc = len(tc_values)
manual_average = sum_tc / count_tc

print(f"--- Verification for Column: {test_col} ---")
print(f"Number of genes with a '1': {count_tc}")
print(f"Sum of their TC values: {sum_tc}")
print(f"Manual Average: {manual_average}")

# Show genes that are predictors (value 1) but have no Entrez ID
missing_info = df[df['entrezgene_id_human'].isna()]
print(f"Number of genes without an Entrez ID: {len(missing_info)}")
print("Sample of genes missing IDs:")
print(missing_info.index[:10].tolist())