import pandas as pd

df = pd.read_csv('data/air_quality.csv')

print("DATA TERATAS")
print(df.head())

print("\n NAMA KOLOM DATA")
print(df.columns)

print("\n INFO DATA TERKINI")
print(df.info())