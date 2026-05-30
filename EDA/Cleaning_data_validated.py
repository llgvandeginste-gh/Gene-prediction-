import pandas as pd

input_file = r'C:\Users\ilseh\Downloads\unique_genes_expression_only.csv'
output_file = 'fully_cleaned_data_validated.csv'

def dual_filter_with_validation(path_in, path_out):
    # 1. Load Data
    df = pd.read_csv(path_in, index_col=0)
    
    # 2. Filtering
    # Filter Genes (Rows)
    gene_mask = (df.mean(axis=1) > 0) & (df.std(axis=1) > 0)
    df_cleaned = df[gene_mask].copy()
    
    # Filter Samples (Columns)
    sample_mask = (df_cleaned.mean(axis=0) > 0) & (df_cleaned.std(axis=0) > 0)
    df_final = df_cleaned.loc[:, sample_mask].copy()

    # 3. THE VALIDATION CHECK
    # We find the smallest mean among all genes in the final set
    min_gene_mean = df_final.mean(axis=1).min()
    zeros_remaining = (df_final.mean(axis=1) == 0).sum()

    print("--- Validation Report ---")
    if zeros_remaining == 0:
        print(f"✅ Success! There are 0 genes with a mean of exactly zero.")
        print(f"   The lowest mean expression found is: {min_gene_mean:.6f}")
    else:
        print(f"⚠️ Warning: There are still {zeros_remaining} genes with a mean of zero.")

    # 4. Save
    df_final.to_csv(path_out)
    print(f"--- Process Complete. Saved to {path_out} ---")

if __name__ == "__main__":
    dual_filter_with_validation(input_file, output_file)