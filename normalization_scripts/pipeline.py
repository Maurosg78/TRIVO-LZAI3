#!/usr/bin/env python
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import joblib

def main():
    # 1. Cargar el dataset con la columna score_aceptacion
    df = pd.read_csv("final_dataset_with_score.csv", low_memory=False)

    # 2. Seleccionar features (por ejemplo, Carbs_g_100g, Fat_g_100g, etc.)
    #    Ajusta según tus necesidades
    X = df[["Carbs_g_100g", "Fat_g_100g"]]  # Ejemplo

    # 3. Definir la variable objetivo
    y = df["score_aceptacion"]  # <-- Ya existe tras el merge

    # 4. Separar en train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 5. Definir pipeline
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor(random_state=42))
    ])

    # 6. Hiperparámetros para el grid
    param_grid = {
        "model__n_estimators": [100, 200],
        "model__max_depth": [None, 10, 20],
        "model__min_samples_split": [2, 5],
    }

    # 7. GridSearchCV
    grid_search = GridSearchCV(
        pipeline, param_grid, cv=3, scoring="neg_mean_squared_error", n_jobs=-1
    )

    # 8. Entrenar
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)

    # 9. Métricas
    r2 = r2_score(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    print("Mejor configuración:", grid_search.best_params_)
    print("R² en test:", r2)
    print("RMSE en test:", rmse)

    # 10. Guardar modelo
    joblib.dump(best_model, "best_random_forest_model.pkl")
    print("Modelo guardado en 'best_random_forest_model.pkl'")

if __name__ == "__main__":
    main()
