import pandas as pd

file_path = '/Users/kelvin/Downloads/archive/2019-Nov.csv'

df = pd.read_csv(file_path)

df['event_time'] = pd.to_datetime(df['event_time'])

earliest_timestamp = df['event_time'].min()
latest_timestamp = df['event_time'].max()

time_span = latest_timestamp - earliest_timestamp

print("Earliest Timestamp:", earliest_timestamp)
print("Latest Timestamp:", latest_timestamp)
print("Time Span Covered by the Dataset:", time_span)
