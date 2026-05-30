import pandas as pd

# 1. Load the data
print("Reading large datafile...")
# sep='\t' for TSV; index_col=0 keeps your Gene names as the row identifiers
df = pd.read_csv(r'C:\Users\ilseh\Downloads\ica_flipped_independent_components_consensus.tsv', sep='\t', index_col=0)

print("Calculating statistics...")

# 2. Create the two summary columns directly
# We perform the comparison and the sum in one step to save memory
total_above_3 = (df >= 3).sum(axis=1)
any_above_3 = (total_above_3 > 0).astype(int)

# 3. Combine them into a small, new DataFrame
summary_df = pd.DataFrame({
    'Total_Above_3': total_above_3,
    'Any_Above_3': any_above_3
})

# 4. Save only the summary to a new TSV file
print("Saving summary file...")
summary_df.to_csv('TC_summary_only.tsv', sep='\t')

print("Success! 'TC_summary_only.tsv' is ready.")
