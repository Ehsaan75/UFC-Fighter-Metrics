from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import unittest
import pandas as pd

class TestModelTraining(unittest.TestCase):

    def setUp(self):
        # Set up mock data for model training
        self.df = pd.DataFrame({
            'strikes_per_min': [5.3, 2.6, 3.4, 6.8, 4.9],
            'striking_accuracy': [0.5, 0.6, 0.5, 0.6, 0.4],
            'wins': [10, 15, 22, 8, 4],
            'losses': [5, 1, 10, 5, 3],
            'high_success': [0, 1, 1, 0, 0]
        })
        self.X = self.df[['strikes_per_min', 'striking_accuracy']]
        self.y = self.df['high_success']

    def test_model_training(self):
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=42)

        # Initialise and train the Random Forest model
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        # Test that the model can make predictions
        y_pred = model.predict(X_test)
        self.assertEqual(len(y_pred), len(y_test))

if __name__ == '__main__':
    unittest.main()
