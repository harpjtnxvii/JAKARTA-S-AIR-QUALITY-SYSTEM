import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

df = pd.read_csv('data/air_quality.csv')

df = df[df['category'] != 'TIDAK ADA DATA']

df['category'] = df['category'].replace({
    'VERY_UNHEALTHY': 'UNHEALTHY'
})

cols = ['PM10', 'PM25', 'SO2', 'CO', 'O3', 'NO2', 'max']
for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna()

features = ['PM10', 'PM25', 'SO2', 'CO', 'O3', 'NO2']
target = 'category'

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=8,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    class_weight='balanced'
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("DISTRIBUSI TARGET:")
print(y.value_counts())

print("\nACCURACY:")
print(accuracy_score(y_test, y_pred))

print("\nCLASSIFICATION REPORT:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nTRAIN SCORE:")
print(model.score(X_train, y_train))

print("\nTEST SCORE:")
print(model.score(X_test, y_test))

with open('model/model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("\nMODEL BERHASIL DISIMPAN KE: model/model.pkl")