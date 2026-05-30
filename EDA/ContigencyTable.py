import pandas as pd 
import numpy as np

df = pd.read_csv(r'C:\Users\ilseh\OneDrive\Documenten\Data_files_RP\10_merged_174libs_samples.txt', sep='\t')

Tissue = ['BAT', 'WAT', 'Heart', 'Kidney', 'Liver', 'Hippoc', 'Cortex', 'Cereb', 'Hypoth']
Group = ['TL', 'TE', 'AL', 'AE','SE']
Sex = ['F', 'M']

# 2. CREATE THE CONTINGENCY TABLE
#print("I found these columns in your file:", df.columns.tolist())
# index: The variables on the left (Sex first, then Tissue)
# columns: The variable across the top (Stage)
contingency_table = pd.crosstab(
    index=[df['Sex'], df['Tissue']], 
    columns=df['Group'], 
    margins=True,
    margins_name="Total"
       )        # Adds the 'Total' row/column
   

print("Contingency Table: Sex & Tissue vs. Group")
print(contingency_table)

mean_weight = df['Weight'].mean()
print(f"The mean weight is: {mean_weight}")

median_weight = df['Weight'].median()
print(f"The median weight is: {median_weight}")

min_weight = df['Weight'].min()
print(f"The minimum weight is: {min_weight}")

max_weight = df['Weight'].max()
print(f"The maximum weight is: {max_weight}")

sd_weight = df['Weight'].std()
print(f"The standard deviation for age is: {sd_weight}")

mean_age = df['Age'].mean()
print(f"The mean age is: {mean_age}")

median_age = df['Age'].median()
print(f"The median age is: {median_age}")

min_age = df['Age'].min()
print(f"The minimum age is: {min_age}")

max_age = df['Age'].max()
print(f"The maximum age is: {max_age}")

sd_age = df['Age'].std()
print(f"The standard deviation for age is: {sd_age}")

df['Weight'] = df['Weight'].apply(lambda x: '>= 86.9' if x >= 86.9 else '< 86.9')
df['Age'] = df['Age'].apply(lambda x: '> 9 days' if x > 9 else '<= 9 days')


table_sex = pd.crosstab(index=[df['Sex'], ['Tissue']], columns=df['Group'], margins=True)
table_weight = pd.crosstab(index=[df['Weight'], df['Group']],  columns=df['Group'], margins=True)
table_age = pd.crosstab(index=[df['Age'], df['Group']], columns=df['Group'], margins=True)

# 4. Save to one Excel file with tables side-by-side
with pd.ExcelWriter('Mouse_Seperate_Contingency_Tables.xlsx') as writer:
    # We use 'startcol' to place them next to each other

    table_sex.to_excel(writer, sheet_name='Summary', startrow=0, startcol=7)
    table_weight.to_excel(writer, sheet_name='Summary', startrow=0, startcol=14) # Moves 7 columns to the right
    table_age.to_excel(writer, sheet_name='Summary', startrow=0, startcol=21) # Moves 14 columns to the right

print("Excel file 'Mouse_Seperate_Contingency_Tables.xlsx' has been created!")