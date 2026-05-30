import pandas as pd


df = pd.read_csv('10_merged_174libs_samples.txt', sep='\t')


df['Weight_Quartile'] = pd.qcut(df['Weight'], q=4, precision=1)
df['Age_Quartile'] = pd.qcut(df['Age'], q=4, precision=1)


table_sex = df['Sex'].value_counts().reset_index()
table_group = df['Group'].value_counts().reset_index()
table_tissue = df['Tissue'].value_counts().reset_index()
table_weight_q = df['Weight_Quartile'].value_counts().sort_index().reset_index()
table_age_q = df['Age_Quartile'].value_counts().sort_index().reset_index()

with pd.ExcelWriter('Single_Variable_Summaries.xlsx', engine='openpyxl') as writer:
    table_sex.to_excel(writer, sheet_name='Counts', startrow=1, startcol=0, index=False)
    table_group.to_excel(writer, sheet_name='Counts', startrow=1, startcol=4, index=False)
    table_tissue.to_excel(writer, sheet_name='Counts', startrow=1, startcol=8, index=False)
    table_weight_q.to_excel(writer, sheet_name='Counts', startrow=1, startcol=12, index=False)
    table_age_q.to_excel(writer, sheet_name='Counts', startrow=1, startcol=16, index=False)
    
    ws = writer.sheets['Counts']
    ws['A1'], ws['E1'], ws['I1'], ws['M1'] = 'Sex Counts', 'Group Counts', 'Weight Quartiles', 'Age Quartiles'