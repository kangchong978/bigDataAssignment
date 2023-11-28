import pandas as pd

file_path = '/Users/kelvin/Downloads/archive/2019-Nov.csv'

df = pd.read_csv(file_path)

df['event_time'] = pd.to_datetime(df['event_time'])

event_type_counts = df['event_type'].value_counts()

print("Frequency of Each Event Type:")
print(event_type_counts)

df['day_of_week'] = df['event_time'].dt.day_name()

daily_event_type_counts = df.pivot_table(index='day_of_week', columns='event_type', aggfunc='size', fill_value=0)

print("\nDaily Event Type Counts:")
print(daily_event_type_counts)
