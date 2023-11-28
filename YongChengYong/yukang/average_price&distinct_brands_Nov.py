import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load data from CSV file
data = pd.read_csv('./archive/2019-Nov.csv')

# 1. Remove rows with NaN values in 'brand' or 'price'
data = data.dropna(subset=['brand', 'price'])

# Group data by user_id and brand
grouped_data = data.groupby(['user_id', 'brand'])

# Count the occurrences of each brand for each user
brand_counts = grouped_data.size().reset_index(name='brand_count')

# Calculate the total event price for each user and brand
total_price = grouped_data['price'].sum().reset_index(name='total_price')

# Merge the two dataframes on user_id and brand
result = pd.merge(brand_counts, total_price, on=['user_id', 'brand'])

# Calculate average event price for each user and brand
result['average_price'] = result['total_price'] / result['brand_count']

# 2. Calculate the total count of distinct brands for each user
distinct_brands_per_user = data.groupby('user_id')['brand'].nunique().reset_index(name='distinct_brands')
result = pd.merge(result, distinct_brands_per_user, on='user_id')

# Subset the relevant columns for K-means clustering
features = result[['average_price', 'distinct_brands']].values

#######

# Try different values of k
k_values = range(1, 11)
wcss_values = []

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(features)
    wcss_values.append(kmeans.inertia_)

# Plot the elbow curve
plt.plot(k_values, wcss_values, marker='o')
plt.title('Elbow Curve')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
plt.show()

#######

# Chosen value of k based on the elbow method
chosen_k = 2  # Change this to the optimal k value

# Perform k-means clustering with the chosen k value
kmeans = KMeans(n_clusters=chosen_k, random_state=42)
result['cluster'] = kmeans.fit_predict(features)

# Visualize the clustering results
plt.scatter(result['average_price'], result['distinct_brands'], c=result['cluster'], cmap='viridis', alpha=0.5)
plt.title('K-Means Clustering Results')
plt.xlabel('Average Price')
plt.ylabel('Distinct Brands Count')
plt.show()
