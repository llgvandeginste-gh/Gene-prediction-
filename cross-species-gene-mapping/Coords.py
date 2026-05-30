import pandas as pd
import requests
import gzip
import io

# 1. Load your consolidated unique gene list
df_unique = pd.read_csv('dormouse_final_consolidated_unique_genes.csv')

# 2. Standardize Entrez IDs for matching
# We convert them to strings to ensure they match the text in the GFF file
entrez_col = 'entrezgene_id_human'
df_unique[entrez_col] = pd.to_numeric(df_unique[entrez_col], errors='coerce').fillna(0).astype(int).astype(str)
target_entrez = set(df_unique[entrez_col].unique())

# 3. Download and Parse Human Coordinates (GRCh38.p14)
print("Downloading Human Coordinates from NCBI (GRCh38.p14)...")
gff_url = "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_genomic.gff.gz"

gene_coords = []
response = requests.get(gff_url, stream=True)

# Process the file in memory without saving to disk
with gzip.open(io.BytesIO(response.content), 'rt') as f:
    for line in f:
        # We only care about rows defining a 'gene'
        if line[0] == '#' or '\tgene\t' not in line:
            continue
            
        parts = line.split('\t')
        attributes = parts[8]
        
        # Look for the GeneID (Entrez ID) in the attributes column
        if 'GeneID:' in attributes:
            eid = attributes.split('GeneID:')[1].split(',')[0].split(';')[0]
            
            # If this Human gene is in our unique list, extract its location
            if eid in target_entrez and 'NC_' in parts[0]:
                gene_coords.append({
                    'GeneID': eid,
                    'Chromosome': parts[0],
                    'BP_Start': parts[3],
                    'BP_End': parts[4],
                    'Strand': parts[6]
                })

# 4. Create a lookup table and merge
coords_lookup = pd.DataFrame(gene_coords).drop_duplicates(subset=['GeneID'])
df_final = pd.merge(df_unique, coords_lookup, left_on=entrez_col, right_on='GeneID', how='left')

# Drop the helper column
if 'GeneID' in df_final.columns:
    df_final = df_final.drop(columns=['GeneID'])

# 5. Save the final annotated file
output_name = 'dormouse_final_unique_with_coordinates_2.csv'
df_final.to_csv(output_name, sep='\t', index=False)


# --- FINAL SUMMARY ---
print("\n" + "="*45)
print("--- COORDINATE MAPPING SUMMARY ---")
print(f"Total Unique Genes:           {len(df_unique)}")
print(f"Genes with Coords Found:      {df_final['Chromosome'].notna().sum()}")
print(f"Genes without Coords Found:   {df_final['Chromosome'].isna().sum()}")
print("-" * 45)
print(f"Final file created: {output_name}")
print("="*45)


