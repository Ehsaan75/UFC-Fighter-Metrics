import unittest
import pandas as pd

class TestDataPreparation(unittest.TestCase):

    def setUp(self):
        # Set up a mock DataFrame for testing
        self.df = pd.DataFrame({
            'striking_accuracy': ['50%', '60%', '70%'],
            'striking_defense': ['40%', '55%', '60%'],
            'wins': [10, 15, 5],
            'losses': [5, 1, 5]
        })
        # Convert percentage columns to decimal
        self.df['striking_accuracy'] = self.df['striking_accuracy'].str.replace('%', '').astype(float) / 100
        self.df['striking_defense'] = self.df['striking_defense'].str.replace('%', '').astype(float) / 100
        # Calculate win percentage
        self.df['win_percentage'] = (self.df['wins'] / (self.df['wins'] + self.df['losses'])) * 100
        # Set success threshold and add high success column
        success_threshold = 70
        self.df['high_success'] = (self.df['win_percentage'] >= success_threshold).astype(int)

    def test_percentage_conversion(self):
        # Test if percentage columns are converted to decimals
        self.assertEqual(self.df['striking_accuracy'].iloc[0], 0.5)
        self.assertEqual(self.df['striking_defense'].iloc[1], 0.55)

    def test_win_percentage(self):
        # Test if win percentage is calculated correctly
        self.assertAlmostEqual(self.df['win_percentage'].iloc[0], 66.6667, places=4)

    def test_high_success(self):
        # Test if the high success column is correctly populated based on win percentage
        success_threshold = 70
        self.assertEqual(self.df['high_success'].iloc[0], 0)  # 66.6667 < 70, so it should be 0

if __name__ == '__main__':
    unittest.main()
