import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from pymongo import MongoClient

# Connect to the MongoDB instance running on localhost at port 27017
client = MongoClient('localhost', 27017)

# Access or create a database named 'mydatabase'
db = client['myFirstDatabase']

# Access collections
collection_oct2019 = db['oct2019']
collection_nov2019 = db['nov2019']

# Query data from MongoDB for October 2019
cursor_oct2019 = collection_oct2019.find({'event_type': 'purchase'})
only_purchases_oct2019 = pd.DataFrame(list(cursor_oct2019))
user_purchase_count_oct2019 = only_purchases_oct2019['user_id'].value_counts().head(100)

# Query data from MongoDB for November 2019
cursor_nov2019 = collection_nov2019.find({'event_type': 'purchase'})
only_purchases_nov2019 = pd.DataFrame(list(cursor_nov2019))
user_purchase_count_nov2019 = only_purchases_nov2019['user_id'].value_counts().head(100)

# Combine the data for the top 100 user purchases
user_purchase_count_combined = pd.concat([user_purchase_count_oct2019, user_purchase_count_nov2019], axis=1)
user_purchase_count_combined.columns = ['Oct 2019', 'Nov 2019']

# Sort the combined data by the sum of purchases and select the top 100
user_purchase_count_combined['Total'] = user_purchase_count_combined.sum(axis=1)
user_purchase_count_combined = user_purchase_count_combined.sort_values(by='Total', ascending=False).head(100)


# Linear regression
x = range(1, len(user_purchase_count_combined) + 1)
y = user_purchase_count_combined['Total']

slope, intercept, r, p, std_err = stats.linregress(x, y)

def findCustomerValue(x):
  return slope * x + intercept

mymodel = list(map(findCustomerValue, x))

valCust = findCustomerValue(1)
print(valCust)

# Create separate scatter plots for each month
plt.figure(figsize=(100, 6))

# Scatter plot for October 2019
plt.scatter(range(1, len(user_purchase_count_combined) + 1), user_purchase_count_combined['Oct 2019'], label='Oct 2019', color='skyblue', alpha=0.7)

# Scatter plot for November 2019
plt.scatter(range(1, len(user_purchase_count_combined) + 1), user_purchase_count_combined['Nov 2019'], label='Nov 2019', color='orange', alpha=0.7)

# Linear regression line
plt.plot(x, mymodel, label='Linear Regression', color='green')

# Set x-axis tick labels to the actual user IDs
plt.xticks(range(1, len(user_purchase_count_combined) + 1), user_purchase_count_combined.index, rotation='vertical')

plt.title('Top 100 cumulative user purchases - Oct and Nov 2019')
plt.xlabel('User ID')
plt.ylabel('Number of Sales')
plt.legend()

plt.show()

