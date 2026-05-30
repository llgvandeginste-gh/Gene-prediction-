import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('mouse_genes_with_coordinates.csv')

def prepare_global_positions(df, chr_col, pos_col, prefix):
    """
    Zet chromosoom-specifieke posities om naar één doorlopende as voor de hele soort.
    """
    # Verwijder rijen zonder coördinaten
    temp_df = df.dropna(subset=[chr_col, pos_col]).copy()
    
    # Sorteer chromosomen logisch (1, 2, 3... X, Y)
    temp_df[chr_col] = temp_df[chr_col].astype(str)
    chroms = sorted(temp_df[chr_col].unique(), key=lambda x: (len(x), x))
    
    cumulative_pos = 0
    offsets = {}
    
    for chrom in chroms:
        offsets[chrom] = cumulative_pos
        # Pak de hoogste waarde van dit chromosoom om de lengte te schatten
        chrom_max = temp_df[temp_df[chr_col] == chrom][pos_col].astype(float).max()
        cumulative_pos += chrom_max
        
    temp_df[f'{prefix}_global'] = temp_df.apply(lambda row: float(row[pos_col]) + offsets[row[chr_col]], axis=1)
    return temp_df, offsets

# 2. Bereken de globale posities voor de assen
# Gebruik jouw specifieke kolomnamen: 'Chromosome' (mens) en 'Mouse_Chromosome' (muis)
df_plot, human_offsets = prepare_global_positions(df, 'Chromosome', 'BP_Start', 'Human')
df_plot, mouse_offsets = prepare_global_positions(df_plot, 'Mouse_Chromosome', 'Mouse_BP_Start', 'Mouse')

# 3. De Synteny Plot maken
plt.figure(figsize=(12, 10))

# We plotten de genen als kleine puntjes
plt.scatter(df_plot['Human_global'], df_plot['Mouse_global'], s=1, color='blue', alpha=0.6)

# Grijze lijnen trekken voor de grenzen tussen chromosomen (Mens - X-as)
for chrom, offset in human_offsets.items():
    plt.axvline(offset, color='lightgrey', linestyle='--', linewidth=0.7)
    # Voeg label toe aan de onderkant
    plt.text(offset, -0.02, chrom, transform=plt.gca().get_xaxis_transform(), fontsize=8, rotation=45)

# Grijze lijnen trekken voor de grenzen tussen chromosomen (Muis - Y-as)
for chrom, offset in mouse_offsets.items():
    plt.axhline(offset, color='lightgrey', linestyle='--', linewidth=0.7)
    # Voeg label toe aan de zijkant
    plt.text(-0.02, offset, chrom, transform=plt.gca().get_yaxis_transform(), fontsize=8)

plt.xlabel('Human Gene Position (Human Chromosomes)', fontweight='bold')
plt.ylabel('Mouse Gene Position (Mouse Chromosomes)', fontweight='bold')
plt.title('Synteny Plot: Locationing of Genes (Human vs Mouse)', fontsize=14)

plt.grid(False) # We hebben onze eigen gridlijnen al getrokken
plt.tight_layout()

# Opslaan en tonen
plt.savefig('synteny_human_mouse.png', dpi=300)
print("De grafiek is opgeslagen als 'synteny_human_mouse.png'")
plt.show()