import pandas as pd

df = pd.read_csv('data/air_quality.csv')

df = df[df['category'] != 'TIDAK ADA DATA']

cols = ['PM10', 'PM25', 'SO2', 'CO', 'O3', 'NO2', 'max']

for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna()

df['date'] = pd.to_datetime(df['date'])

features = ['PM10', 'PM25', 'SO2', 'CO', 'O3', 'NO2']
target = 'category'

X = df[features]
y = df[target]

print("SHAPE DATA BERSIH:")
print(df.shape)

print("\nFITUR YANG DIGUNAKAN:")
print(features)

print("\nSHAPE X:")
print(X.shape)

print("\nSHAPE y:")
print(y.shape)

print("\n5 DATA FITUR TERATAS:")
print(X.head())

print("\n5 DATA TARGET TERATAS:")
print(y.head())

print("\nDISTRIBUSI TARGET:")
print(y.value_counts())