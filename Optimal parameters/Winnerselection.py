import pandas as pd

# 1. Load the final merged file we just created
df = pd.read_csv('top_75_with_average_TC.csv')

# 2. Ensure 'Average_TC' is treated as a number
df['Average_TC'] = pd.to_numeric(df['Average_TC'], errors='coerce')


# 3. Group by Cluster and Ordering Method, then pick the row with max Average_TC
# We sort by Average_TC descending and take the first (highest) for each group
df_winners = (
    df.sort_values(['cluster', 'ordering_method', 'Average_TC'], ascending=[True, True, False])
    .groupby(['cluster', 'ordering_method'])
    .head(1)
    .reset_index(drop=True)
)

# 5. Save the winners
df_winners.to_csv('top_15_tc_winners.csv', index=False)

# 6. Print the winners for a quick summary
print("The 15 Winners (Highest Average TC per method per cluster):")
print(df_winners[['cluster', 'ordering_method', 'median_pearsonr_test', 'Average_TC']])