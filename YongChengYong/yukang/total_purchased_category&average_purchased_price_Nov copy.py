import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load data from CSV file
data = pd.read_csv('./archive/2019-Oct.csv', nrows=30000)

# get all the data chich event_type is "purchase"
purchase_data = data[data['event_type'] == 'purchase']

# Get user_ids with at least one purchase
users_with_purchase = purchase_data['user_id'].unique()

# Filter the original data based on users with at least one purchase
filtered_data = data[data['user_id'].isin(users_with_purchase)]

# Remove rows where either 'category_id' or 'price' is null
filtered_data = filtered_data.dropna(subset=['category_id', 'price'])

# Group by user_id and calculate total purchased categories and average purchased price
user_summary = filtered_data.groupby('user_id').agg({
    'category_id': 'nunique',  # Count unique categories
    'price': 'mean'  # Calculate average price
}).rename(columns={'category_id': 'total_purchased_categories', 'price': 'average_purchased_price'})

# Now, user_summary contains the total purchased categories and average purchased price for each user

# Subset the relevant columns for K-means clustering
features = user_summary[['total_purchased_categories', 'average_purchased_price']].values

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

# Specify the number of clusters (K)
k = 2

# Step 1: Initialize centroids randomly
centroids = features[np.random.choice(range(len(features)), k, replace=False)]

# Plot the initial data and centroids
fig, axes = plt.subplots(2, 6, figsize=(15, 5))  # 2 rows, 6 columns

# Initial state
axes[0, 0].scatter(features[:, 0], features[:, 1], s=50, cmap='viridis')
axes[0, 0].scatter(centroids[:, 0], centroids[:, 1], c='red', marker='X', s=200, label='Initial Centroids')
axes[0, 0].set_title('Initial Data and Centroids')
axes[0, 0].legend()

# K-means algorithm
converged = False
iteration = 1

while not converged:
    # Step 2: Assign each data point to the nearest centroid
    labels = np.argmin(np.linalg.norm(features[:, np.newaxis] - centroids, axis=2), axis=1)

    # Step 3: Update centroids based on the assigned data points
    new_centroids = np.array([features[labels == i].mean(axis=0) for i in range(k)])

    # Plot the current state of the algorithm
    ax = axes.flatten()[iteration]
    ax.scatter(features[:, 0], features[:, 1], c=labels, s=50, cmap='viridis')
    ax.scatter(new_centroids[:, 0], new_centroids[:, 1], c='red', marker='X', s=200, label='Updated Centroids')
    ax.set_title(f'Iteration {iteration}')
    ax.legend()

    # Check for convergence
    converged = np.all(centroids == new_centroids)

    # Update centroids for the next iteration
    centroids = new_centroids
    iteration += 1

plt.tight_layout()  # Adjust layout for better spacing
plt.show()

print(f'Final centroids:\n{centroids}')