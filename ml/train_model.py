# import pandas as pd 

# # load the dataset 
# file_path = "ml/pune_waterlogging_clean.csv.xlsx"
# df = pd.read_excel(file_path) 

# # print all column names 
# print("=== COLUMNS ===")
# print(df.columns.tolist())

# # 2. Print first 5 rows
# print("\n=== FIRST 5 ROWS ===")
# print(df.head()) 

# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from xgboost import XGBClassifier
# from sklearn.metrics import accuracy_score

# # 1. Load dataset
# df = pd.read_excel("ml/pune_waterlogging_clean.csv.xlsx")

# # 2. Select input features (X) and target output (y)
# features = ['latitude', 'longitude', 'ground_elevation_m', 'slope_percentage', 
#             'is_low_lying_basin', 'precipMM', 'humidity']
# X = df[features]
# y = df['Is_Waterlogged']

# # 3. Split into 80% training data and 20% test data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # 4. Train & evaluate Random Forest
# rf_model = RandomForestClassifier(random_state=42)
# rf_model.fit(X_train, y_train)
# rf_acc = accuracy_score(y_test, rf_model.predict(X_test))

# # 5. Train & evaluate XGBoost
# xgb_model = XGBClassifier(random_state=42, eval_metric='logloss')
# xgb_model.fit(X_train, y_train)
# xgb_acc = accuracy_score(y_test, xgb_model.predict(X_test))

# # 6. Print accuracy comparison
# print("\n=== ACCURACY COMPARISON ===")
# print(f"Random Forest Accuracy: {rf_acc * 100:.2f}%")
# print(f"XGBoost Accuracy:       {xgb_acc * 100:.2f}%") 

# """
# ML Model Training Script
# Dataset: Pune Urban Waterlogging
# Algorithm: Random Forest Classifier
# """

# import pandas as pd
# import joblib
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier

# # 1. Load cleaned Pune waterlogging dataset
# df = pd.read_excel("ml/pune_waterlogging_clean.csv.xlsx")

# # 2. Select feature columns and target output variable
# FEATURES = [
#     'latitude', 'longitude', 'ground_elevation_m', 
#     'slope_percentage', 'is_low_lying_basin', 'precipMM', 'humidity'
# ]
# TARGET = 'Is_Waterlogged'

# X = df[FEATURES]
# y = df[TARGET]

# # 3. Train-Test Split (80% training, 20% validation)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # 4. Instantiate and fit Random Forest model
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # 5. Serialize model artifact to ml/ directory
# joblib.dump(model, "ml/waterlogging_model.pkl")
# print("✅ SUCCESS: Trained model saved as ml/waterlogging_model.pkl") 

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# 1. Synthetic dataset setup (Elevation, Slope, Precipitation, Humidity)
np.random.seed(42)
n_samples = 1000
df = pd.DataFrame({
    'elevation': np.random.uniform(500, 600, n_samples),
    'slope': np.random.uniform(0, 15, n_samples),
    'precipitation': np.random.uniform(0, 120, n_samples),
    'humidity': np.random.uniform(40, 100, n_samples)
})
df['waterlogging_risk'] = ((df['elevation'] < 530) & (df['precipitation'] > 50) | (df['slope'] < 2.0) & (df['precipitation'] > 40)).astype(int)

X = df[['elevation', 'slope', 'precipitation', 'humidity']]
y = df['waterlogging_risk']

# 2. Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 3. Export trained binary model for production/backend API
joblib.dump(model, 'ml/waterlogging_rf_model.joblib')
print("Model saved successfully as 'ml/waterlogging_rf_model.joblib'")