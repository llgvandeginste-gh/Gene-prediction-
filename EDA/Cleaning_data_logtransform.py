import pandas as pd
import numpy as np

input_file = r'C:\Users\ilseh\Downloads\unique_genes_expression_only (1).csv'
output_file = 'New_log2_cleaned_data.csv'

def process_gene_data(path_in, path_out):
    # 1. Load Data
    df = pd.read_csv(path_in, index_col=0)
    
    # 2. Filter out invariant genes/samples (as we did before)
    # This removes genes where ALL values are the same or all are zero
    df = df[(df.mean(axis=1) > 0) & (df.std(axis=1) > 0)]
    df = df.loc[:, (df.mean(axis=0) > 0) & (df.std(axis=0) > 0)]

    # 3. Log2(x + 1) Transformation
    # np.log1p(x) is mathematically equivalent to log(1 + x) 
    # but more accurate for very small numbers.
    # We use np.log2 to get the base-2 log specifically.
    log2_df = np.log2(df + 1)

    # 4. Save
    log2_df.to_csv(path_out)
    
    print(f"--- Transformation Complete ---")
    print(f"Original Max Value: {df.values.max():.2f}")
    print(f"New Log2 Max Value: {log2_df.values.max():.2f}")
    print(f"File saved as: {path_out}")

if __name__ == "__main__":
    process_gene_data(input_file, output_file)