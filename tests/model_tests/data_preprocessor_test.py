import unittest
from backend.utils.load_config import load_config
from backend.models.data_preprocessor import load_data_from_s3, normalize_data, convert_to_numpy  # replace `your_module` with the actual module name

class TestDataProcessing(unittest.TestCase):

    def test_load_data_from_s3(self):
        # Note: Make sure the AWS credentials are set up in the environment or AWS config

        # Load configuration
        config = load_config()

        df = load_data_from_s3(config['s3_bucket_name'], config['s3_object_name'])
        self.assertIsNotNone(df)

        # Check if the first row matches expected
        self.assertEqual(df['description'].iloc[0], 'GRANOLA, CINNAMON, RAISIN, CINNAMON, RAISIN')
        self.assertEqual(df['description'].iloc[-1],'Long Life Vegetable Oil 128 ounce')
        

    def test_normalize_data(self):
        # Prepare data
        df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': [4, 5, 6]
        })

        # Test function
        normalized_df, scaler = normalize_data(df, ['col1', 'col2'])
        self.assertIsNotNone(normalized_df)
        self.assertIsNotNone(scaler)

    def test_convert_to_numpy(self):
        # Prepare data
        df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': [4, 5, 6]
        })

        # Test function
        np_array = convert_to_numpy(df, ['col1', 'col2'])
        self.assertIsNotNone(np_array)
        self.assertEqual(np_array.shape, (3, 2))

if __name__ == '__main__':
    unittest.main()
