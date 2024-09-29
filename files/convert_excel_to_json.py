import pandas as pd

# Load the updated Excel file
test_icd = pd.read_excel("last_file.xlsx")

# Convert the DataFrame to a JSON format
# You can specify an orientation; here we use "records" to get a list of dictionaries
test_icd_json = test_icd.to_json(orient="records", force_ascii=False, indent=4)

# Save the JSON data to a file
with open("latest_icd.json", "w", encoding="utf-8") as json_file:
    json_file.write(test_icd_json)

print("Excel file has been successfully converted to JSON")
