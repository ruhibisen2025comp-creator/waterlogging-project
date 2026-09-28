import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

def generate_mock_data(n_samples=500):
    """Generates synthetic geospatial/weather data if local CSV is missing."""
    np.random.seed(42)
    elevation = np.random.uniform(500, 600, n_samples)  # Pune elevation in meters
    slope = np.random.uniform(0, 15, n_samples)          # Terrain slope in degrees
    precip = np.random.uniform(0, 120, n_samples)        # Rainfall in mm
    humidity = np.random.uniform(40, 100, n_samples)     # Humidity %

    # Rule-based risk labeling (1 = Waterlogging, 0 = Normal)
    risk = ((elevation < 530) & (precip > 50) | (slope < 2.0) & (precip > 40)).astype(int)

    return pd.DataFrame({
        'elevation': elevation,
        'slope': slope,
        'precipitation': precip,
        'humidity': humidity,
        'waterlogging_risk': risk
    })

def evaluate_models():
    df = generate_mock_data()
    X = df[['elevation', 'slope', 'precipitation', 'humidity']]
    y = df['waterlogging_risk']

    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": XGBClassifier(n_estimators=100, learning_rate=0.1, eval_metric='logloss', random_state=42)
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']

    print("=" * 60)
    print(" 5-FOLD CROSS-VALIDATION BENCHMARK (PUNE WATERLOGGING MODEL)")
    print("=" * 60)

    results = []

    for name, model in models.items():
        scores = cross_validate(model, X, y, cv=cv, scoring=scoring)

        metrics = {
            "Model": name,
            "Accuracy": f"{scores['test_accuracy'].mean():.4f} (±{scores['test_accuracy'].std():.4f})",
            "Precision": f"{scores['test_precision'].mean():.4f}",
            "Recall": f"{scores['test_recall'].mean():.4f}",
            "F1-Score": f"{scores['test_f1'].mean():.4f}",
            "ROC-AUC": f"{scores['test_roc_auc'].mean():.4f}"
        }
        results.append(metrics)

    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))
    print("=" * 60)

if __name__ == "__main__":
    evaluate_models()