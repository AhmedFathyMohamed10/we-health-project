import pandas as pd

# Load the two Excel files
test_icd = pd.read_excel("next_todo.xlsx")
cat = pd.read_excel("cat.xlsx")

# Clean up the Title column in cat.xlsx to identify levels based on dashes
cat['H_Level'] = cat['Title'].apply(lambda x: x.count('-'))
cat['Title_Clean'] = cat['Title'].str.replace('-', '').str.strip()

# Initialize variables to store the current H1, H2, H3, H4, and H5
current_h1 = None
current_h2 = None
current_h3 = None
current_h4 = None
current_h5 = None

# Create lists to store the H1, H2, H3, H4, and H5 values for each row
h1_list = []
h2_list = []
h3_list = []
h4_list = []
h5_list = []

# Iterate over the rows of cat.xlsx to get the H1, H2, H3, H4, and H5 titles
for index, row in cat.iterrows():
    title = row['Title']
    h_level = row['H_Level']
    chapter_no = row['ChapterNo']
    
    # H1: No dashes (H_Level == 0)
    if h_level == 0:
        current_h1 = row['Title_Clean']
        current_h2 = None  # Reset H2 when a new H1 is found
        current_h3 = None  # Reset H3 when a new H1 is found
        current_h4 = None  # Reset H4 when a new H1 is found
        current_h5 = None  # Reset H5 when a new H1 is found
    
    # H2: One dash (H_Level == 1)
    elif h_level == 1:
        current_h2 = row['Title_Clean']
        current_h3 = None  # Reset H3 when a new H2 is found
        current_h4 = None  # Reset H4 when a new H2 is found
        current_h5 = None  # Reset H5 when a new H2 is found
    
    # H3: Two dashes (H_Level == 2)
    elif h_level == 2:
        current_h3 = row['Title_Clean']
        current_h4 = None  # Reset H4 when a new H3 is found
        current_h5 = None  # Reset H5 when a new H3 is found
    
    # H4: Three dashes (H_Level == 3)
    elif h_level == 3:
        current_h4 = row['Title_Clean']
        current_h5 = None  # Reset H5 when a new H4 is found
    
    # H5: Four dashes (H_Level == 4)
    elif h_level == 4:
        current_h5 = row['Title_Clean']
    
    # Append the current values of H1, H2, H3, H4, and H5 to the lists
    h1_list.append(current_h1)
    h2_list.append(current_h2)
    h3_list.append(current_h3)
    h4_list.append(current_h4)
    h5_list.append(current_h5)

# Add the H1, H2, H3, H4, and H5 lists to the cat DataFrame
cat['H1'] = h1_list
cat['H2'] = h2_list
cat['H3'] = h3_list
cat['H4'] = h4_list
cat['H5'] = h5_list

# Now we will map the H1, H2, H3, H4, and H5 back to the test_icd.xlsx based on the ChapterNo and Code
# Create a dictionary to map chapter numbers and codes to H1, H2, H3, H4, and H5
h_mapping = {}

for _, row in cat.iterrows():
    chapter_no = row['ChapterNo']
    code = row['Code']
    
    # Create a key based on chapter number and code for lookup
    h_mapping[(chapter_no, code)] = {
        'H1': row['H1'],
        'H2': row['H2'],
        'H3': row['H3'],
        'H4': row['H4'],
        'H5': row['H5']
    }

# Initialize the columns for H1, H2, H3, H4, and H5 in test_icd
test_icd['H1'] = None
test_icd['H2'] = None
test_icd['H3'] = None
test_icd['H4'] = None
test_icd['H5'] = None

# Now we will iterate over the test_icd file and assign the H1, H2, H3, H4, and H5 based on the mapping
for index, row in test_icd.iterrows():
    chapter_no = row['Chapter']
    code = row['icd11Code']
    
    # Find the matching H1, H2, H3, H4, and H5 based on the chapter number and code
    h_info = h_mapping.get((chapter_no, code), {})
    
    # Assign H1, H2, H3, H4, and H5 to the test_icd row
    test_icd.at[index, 'H1'] = h_info.get('H1', None)
    test_icd.at[index, 'H2'] = h_info.get('H2', None)
    test_icd.at[index, 'H3'] = h_info.get('H3', None)
    test_icd.at[index, 'H4'] = h_info.get('H4', None)
    test_icd.at[index, 'H5'] = h_info.get('H5', None)

# Make sure to keep 'Title_en' and 'Chapter' columns
# Make sure to use the correct column names
final_columns = ['icd11Code', 'Title_en', 'Chapter', 'H1', 'H2', 'H3', 'H4', 'H5'] + \
                [col for col in test_icd.columns if col not in ['H1', 'H2', 'H3', 'H4', 'H5']]

# Save the updated test_icd.xlsx file with the desired columns
test_icd.to_excel("updated.xlsx", columns=final_columns, index=False)

print("H1, H2, H3, H4, and H5 columns have been successfully updated and saved to updated.xlsx, including Title_en and Chapter.")
