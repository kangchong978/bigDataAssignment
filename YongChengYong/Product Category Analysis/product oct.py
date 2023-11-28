import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 

data_csv = "/Users/kelvin/Downloads/archive/2019-Oct.csv"
raw_data = pd.read_csv(data_csv)

category_code_data = raw_data[['event_type', 'product_id', 'category_code']]

only_purchases = category_code_data[category_code_data['event_type'] == 'purchase']

category_sales_count = only_purchases['category_code'].value_counts().reset_index()
category_sales_count.columns = ['category_code', 'n_sales']

top_10_categories = category_sales_count.head(10)
print(top_10_categories)

plt.figure(figsize=(10, 6))
sns.barplot(x='n_sales', y='category_code', data=category_sales_count.head(10))
plt.title('Top 10 Selling Product Categories')
plt.xlabel('Number of Sales')
plt.ylabel('Product Category')
plt.show()