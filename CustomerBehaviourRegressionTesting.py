import unittest
import pandas as pd
from scipy import stats
from pymongo import MongoClient
import matplotlib.pyplot as plt

class TestLinearRegressionProgram(unittest.TestCase):
    def setUp(self):
        # Accessing MongoDB 
        client = MongoClient('localhost', 27017)
        db = client['myFirstDatabase']

        # Accessing collection
        collection_oct2019 = db['oct2019']
        collection_nov2019 = db['nov2019']

        cursor_oct2019 = collection_oct2019.find({'event_type': 'purchase'})
        only_purchases_oct2019 = pd.DataFrame(list(cursor_oct2019))
        user_purchase_count_oct2019 = only_purchases_oct2019['user_id'].value_counts().head(100)

        cursor_nov2019 = collection_nov2019.find({'event_type': 'purchase'})
        only_purchases_nov2019 = pd.DataFrame(list(cursor_nov2019))
        user_purchase_count_nov2019 = only_purchases_nov2019['user_id'].value_counts().head(100)

        # Combine the data for the top 100 user purchases
        self.user_purchase_count_combined = pd.concat([user_purchase_count_oct2019, user_purchase_count_nov2019], axis=1)
        self.user_purchase_count_combined.columns = ['Oct 2019', 'Nov 2019']

        # Sort the combined data by the sum of purchases and select the top 100
        self.user_purchase_count_combined['Total'] = self.user_purchase_count_combined.sum(axis=1)
        self.user_purchase_count_combined = self.user_purchase_count_combined.sort_values(by='Total', ascending=False).head(100)

        # Linear regression
        self.x = range(1, len(self.user_purchase_count_combined) + 1)
        self.y = self.user_purchase_count_combined['Total']

        self.slope, self.intercept, _, _, _ = stats.linregress(self.x, self.y)

    def test_linear_regression(self):
        # Test linear regression on user purchases
        mymodel = list(map(lambda x: self.slope * x + self.intercept, self.x))

        # Check if the model is correct for a sample point
        valCust = self.slope * 1 + self.intercept
        self.assertAlmostEqual(valCust, mymodel[0], delta=0.001)

    def test_plot_generation(self):
        # Test if the plot is generated without errors
        try:
            # Create plot
            plt.figure(figsize=(100, 6))
            plt.scatter(self.x, self.user_purchase_count_combined['Oct 2019'], label='Oct 2019', color='skyblue', alpha=0.7)
            plt.scatter(self.x, self.user_purchase_count_combined['Nov 2019'], label='Nov 2019', color='orange', alpha=0.7)
            plt.plot(self.x, list(map(lambda x: self.slope * x + self.intercept, self.x)), label='Linear Regression', color='green')
            plt.xticks(self.x, self.user_purchase_count_combined.index, rotation='vertical')
            plt.title('Top 100 cumulative user purchases - Oct and Nov 2019')
            plt.xlabel('User ID')
            plt.ylabel('Number of Sales')
            plt.legend()
            plt.show()
        except Exception as e:
            self.fail(f"Plot generation failed with error: {e}")

if __name__ == '__main__':
    unittest.main()
