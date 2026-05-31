import pandas as pd


df = pd.read_csv(r'C:\Users\ilseh\Downloads\ica_flipped_independent_components_consensus.tsv', sep='\t', index_col=0)



#  Create the two summary columns
total_above_3 = (df >= 3).sum(axis=1)
any_above_3 = (total_above_3 > 0).astype(int)

#  Combine them 
summary_df = pd.DataFrame({
    'Total_Above_3': total_above_3,
    'Any_Above_3': any_above_3
})

# 4. Save only the summary to a new TSV file

summary_df.to_csv('TC_summary_only.tsv', sep='\t')

print("TC_summary_only.tsv' is ready.")
