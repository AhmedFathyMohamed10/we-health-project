import pandas as pd

# Load the data (assuming the file is an Excel file with a sheet name, adjust accordingly for CSV)
# Replace 'your_file.xlsx' and 'Sheet1' with the correct file path and sheet name
df = pd.read_excel('UPDATED_ICDs.xlsx', sheet_name='Sheet1')

# Step 1: Add a unique 'flagH1' column based on distinct values of 'H1'
# Get distinct H1 values and assign a unique index to them
df['flagH1'] = df.groupby('H1').ngroup() + 1

# Step 2: Create a combined column from 'icd9Code', 'icd10Code', 'icd11Code', separated by '&'
df['CombinedCodes'] = df[['icd9Code', 'icd10Code', 'icd11Code']].apply(lambda x: '&'.join(x.dropna()), axis=1)

# Step 3: Output the final dataframe (you can export it or view it)
print(df.head())

# Optionally, save the final dataframe to a new Excel file
df.to_excel('updated_icd_table.xlsx', index=False)
