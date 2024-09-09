import pandas as pd

# Load the two Excel files
test_icd = pd.read_excel("test_icd.xlsx")
cat = pd.read_excel("cat.xlsx")

# Clean up the Title column in cat.xlsx to identify levels based on dashes
cat['H_Level'] = cat['Title'].apply(lambda x: x.count('-'))
cat['Title_Clean'] = cat['Title'].str.replace('-', '').str.strip()

# Initialize variables to store the current H1, H2, and H3
current_h1 = None
current_h2 = None
current_h3 = None

# Create lists to store the H1, H2, and H3 values for each row
h1_list = []
h2_list = []
h3_list = []

# Iterate over the rows of cat.xlsx to get the H1, H2, and H3 titles
for index, row in cat.iterrows():
    title = row['Title']
    h_level = row['H_Level']
    chapter_no = row['ChapterNo']
    
    # H1: No dashes (H_Level == 0)
    if h_level == 0:
        current_h1 = row['Title_Clean']
        current_h2 = None  # Reset H2 when a new H1 is found
        current_h3 = None  # Reset H3 when a new H1 is found
    
    # H2: One dash (H_Level == 1)
    elif h_level == 1:
        current_h2 = row['Title_Clean']
        current_h3 = None  # Reset H3 when a new H2 is found
    
    # H3: Two dashes (H_Level == 2)
    elif h_level == 2:
        current_h3 = row['Title_Clean']
    
    # Append the current values of H1, H2, and H3 to the lists
    h1_list.append(current_h1)
    h2_list.append(current_h2)
    h3_list.append(current_h3)

# Add the H1, H2, and H3 lists to the cat DataFrame
cat['H1'] = h1_list
cat['H2'] = h2_list
cat['H3'] = h3_list

# Now we will map the H1, H2, and H3 back to the test_icd.xlsx based on the ChapterNo and Code
# Create a dictionary to map chapter numbers and codes to H1, H2, H3
h_mapping = {}

for _, row in cat.iterrows():
    chapter_no = row['ChapterNo']
    code = row['Code']
    
    # Create a key based on chapter number and code for lookup
    h_mapping[(chapter_no, code)] = {
        'H1': row['H1'],
        'H2': row['H2'],
        'H3': row['H3']
    }

# Initialize the columns for H1, H2, H3 in test_icd
test_icd['H1'] = None
test_icd['H2'] = None
test_icd['H3'] = None

# Now we will iterate over the test_icd file and assign the H1, H2, H3 based on the mapping
for index, row in test_icd.iterrows():
    chapter_no = row['Chapter']
    code = row['Code']
    
    # Find the matching H1, H2, H3 based on the chapter number and code
    h_info = h_mapping.get((chapter_no, code), {})
    
    # Assign H1, H2, and H3 to the test_icd row
    test_icd.at[index, 'H1'] = h_info.get('H1', None)
    test_icd.at[index, 'H2'] = h_info.get('H2', None)
    test_icd.at[index, 'H3'] = h_info.get('H3', None)

# Make sure to keep 'Title_en' and 'Chapter' columns
final_columns = ['Code', 'Title_en', 'Chapter', 'H1', 'H2', 'H3'] + [col for col in test_icd.columns if col not in ['H1', 'H2', 'H3']]

# Save the updated test_icd.xlsx file with the desired columns
test_icd.to_excel("updated_test_icd2.xlsx", columns=final_columns, index=False)

print("H1, H2, and H3 columns have been successfully updated and saved to updated_test_icd.xlsx, including Title_en and Chapter.")
