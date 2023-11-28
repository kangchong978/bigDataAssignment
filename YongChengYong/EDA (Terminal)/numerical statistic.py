import pandas as pd

file_path = '/Users/kelvin/Downloads/archive/2019-Nov.csv'

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(file_path)

mean_value = df['price'].mean()
median_value = df['price'].median()
std_deviation = df['price'].std()
data_range = df['price'].max() - df['price'].min()

print("Mean:", mean_value)
print("Median:", median_value)
print("Standard Deviation:", std_deviation)
print("Range:", data_range)
