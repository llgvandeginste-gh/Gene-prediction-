import pandas as pd
from sklearn.model_selection import train_test_split

# 1. Which cluster file are you processing? 
# Change this for each run (e.g., 'gene_cluster_2_expression.csv', etc.)
input_file = r'new_log_gene_cluster_1_expression.csv'
cluster_name = 'new_log_cluster_1'

# 2. Load the cluster data
df = pd.read_csv(input_file, index_col=0)

# 3. Split the data
# train_size=0.8 sets the split to 80% Training / 20% Testing
# random_state=42 ensures that if you run this again, you get the same "random" split
train_df, test_df = train_test_split(df, train_size=0.8, random_state=42)

# 4. Save the new files
train_filename = f'{cluster_name}_training_80.csv'
test_filename = f'{cluster_name}_testing_20.csv'

train_df.to_csv(train_filename)
test_df.to_csv(test_filename)

# 5. Summary Printout
print(f"--- Processing {input_file} ---")
print(f"Total genes: {len(df)}")
print(f"Saved {len(train_df)} genes to {train_filename}")
print(f"Saved {len(test_df)} genes to {test_filename}")
print("Done!\n")