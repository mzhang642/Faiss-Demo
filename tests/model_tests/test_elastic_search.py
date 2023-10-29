import unittest
import os
import pandas as pd
from elasticsearch import Elasticsearch
from backend.utils.load_config import load_config
from backend.models.elastic_search import initialize_elasticsearch, perform_fuzzy_search

class TestElasticSearchModel(unittest.TestCase):

    def setUp(self):
        try:
            current_dir = os.path.dirname(__file__)  # get current directory
            csv_file_path = os.path.join(current_dir, "..", "..", "data", "sampled_dataset.csv")
            self.df = pd.read_csv(csv_file_path)
            print("Successfully read the CSV into a DataFrame.")
            # print(self.df.head())  # print first 5 rows to verify
        except FileNotFoundError:
            print(f"File not found at {csv_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

        try:
            # Load configuration
            self.config = load_config()
        except Exception as e:
            print(f"Failed to load config: {e}")

        # Initialize your Elasticsearch index with data
        self.es = initialize_elasticsearch(self.df, self.config['elasticsearch_host'])

    # def test_perform_fuzzy_search(self):
    #     # Test the perform_fuzzy_search method
    #     matches = perform_fuzzy_search(self.es, 'appl', 'test_food')
    #     self.assertEqual(len(matches), 1)
    #     self.assertEqual(matches[0]['name'], 'apple')
        
    #     # Test with no matches
    #     matches = perform_fuzzy_search(self.es, 'xyz', 'test_food')
    #     self.assertEqual(len(matches), 0)
    def test_initialize_elasticsearch(self):
        self.assertIsInstance(self.es, Elasticsearch, "Initialization of Elasticsearch failed.")

    # def tearDown(self):
    #     # Optionally, you can delete the test index to clean up
    #     self.es.indices.delete(index='test_food', ignore=[400, 404])
    def test_perform_fuzzy_search(self):
        # Assuming 'description' column exists and contains the word "apple"
        query_data = "aplpe"  # intentionally misspelled to test fuzzy search
        matches = perform_fuzzy_search(self.es, query_data)

        self.assertIsNotNone(matches, "Fuzzy search returned None.")
        self.assertTrue(any("apple" in match["name"].lower() for match in matches), "Fuzzy search did not return expected result.")

if __name__ == '__main__':
    print("Tests are about to run")
    unittest.main()
    print("Tests have completed")

