from pymongo import MongoClient, errors

class MongoDBHandler:
    def __init__(self, db_name='mic_db', mongo_url='mongodb://localhost:27017/'):
        self.client = MongoClient(mongo_url)
        self.db = self.client[db_name]
        self.collection = self.db['drugs_coll']
        self.matching_collection = self.db['matching_data']
        self.varied_collection = self.db['varied_data']

    def has_same_keys(self, doc1, doc2):
        keys_doc1 = set(doc1.keys())
        keys_doc2 = set(doc2.keys())
        return keys_doc1 == keys_doc2

    def categorize_documents(self):
        try:
            # Fetch all documents from the collection
            documents = list(self.collection.find())

            # Initialize lists for matching and varied documents
            matching_documents = []
            varied_documents = []

            # Iterate through documents to categorize
            for i in range(len(documents)):
                current_doc = documents[i]
                matched = False

                # Check against subsequent documents
                for j in range(i + 1, len(documents)):
                    next_doc = documents[j]

                    # Compare structures
                    if self.has_same_keys(current_doc, next_doc):
                        if not matched:
                            matching_documents.append(current_doc)
                            matched = True
                        matching_documents.append(next_doc)
                    else:
                        varied_documents.append(current_doc)
                        break  # Break as soon as a variation is found

            # Insert categorized documents into respective collections
            for doc in matching_documents:
                try:
                    self.matching_collection.insert_one(doc)
                except errors.DuplicateKeyError:
                    continue  

            for doc in varied_documents:
                try:
                    self.varied_collection.insert_one(doc)
                except errors.DuplicateKeyError:
                    continue  

            # Print summaries
            print(f"Inserted {len(matching_documents)} documents into 'matching_data' collection.")
            print(f"Inserted {len(varied_documents)} documents into 'varied_data' collection.")

        except Exception as e:
            print(f"Error categorizing documents: {e}")

    def close_connection(self):
        self.client.close()


# Example usage:
if __name__ == "__main__":
    # Initialize the MongoDBHandler instance
    mongo_handler = MongoDBHandler()

    # Categorize documents
    mongo_handler.categorize_documents()

    # Close MongoDB client connection
    mongo_handler.close_connection()
