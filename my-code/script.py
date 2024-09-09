import os
import ijson
import json

def extract_sample_from_directory(input_dir, output_dir):
    num_items = 200  # predefined number of items to extract
    file_count = 1

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, f'standard_sample_{file_count}.json')

            sample = []
            with open(input_file, 'r') as infile:
                items = ijson.items(infile, 'item')
                for _, item in zip(range(num_items), items):
                    sample.append(item)

            with open(output_file, 'w') as outfile:
                json.dump(sample, outfile, indent=4)

            file_count += 1

input_directory = 'JSONs'
output_directory = 'sample json outputs'
print("starting ............")
extract_sample_from_directory(input_directory, output_directory)




# Run git Doc






























