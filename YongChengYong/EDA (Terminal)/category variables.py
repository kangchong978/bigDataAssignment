import pandas as pd

file_path = '/Users/kelvin/Downloads/archive/2019-Nov.csv'

df = pd.read_csv(file_path)

unique_values_count = df[['event_type', 'category_code', 'brand']].nunique()

event_type_counts = df['event_type'].value_counts()
category_code_counts = df['category_code'].value_counts()
brand_counts = df['brand'].value_counts()

print("Count of Unique Values:")
print(unique_values_count)

print("\nFrequency Distribution for 'event_type':")
print(event_type_counts)

print("\nFrequency Distribution for 'category_code':")
print(category_code_counts)

print("\nFrequency Distribution for 'brand':")
print(brand_counts)
