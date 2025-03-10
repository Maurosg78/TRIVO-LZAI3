#!/usr/bin/env python
"""
Script para entrenar un RandomForestRegressor a partir de un CSV que contiene
columnas de proporciones de ingredientes (prefijo 'porc_') y una columna de score
(p.ej., 'score_aceptacion'). Realiza limpieza de valores problemáticos:
- 'traces' -> '0'
- '15,3'   -> '15.3'

Luego, divide los datos en train/test, ejecuta un GridSearchCV y guarda el mejor
modelo en 'best_random_forest_model.pkl'.
"""

import sys
import re

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import joblib

def preprocess_numeric_columns(df, columns):
    """
    Convierte las columnas especificadas a formato numérico de forma robusta:
      1. Convierte a string, elimina saltos de línea y espacios, y pasa a minúsculas.
      2. Reemplaza 'trace' o 'traces' por '0'.
      3. Reemplaza comas por puntos (ej. '15,3' -> '15.3').
      4. Elimina caracteres no numéricos, excepto dígitos, punto y signo menos.
      5. Convierte a float, forzando errores a NaN.
    """
    def clean_value(x):
        s = str(x).strip().lower()
        s = s.replace('\n', '')
        # Reemplazar 'trace' o 'traces' por '0'
        s = re.sub(r'\btraces?\b', '0', s)
        # Cambiar comas por puntos
        s = s.replace(',', '.')
        # Eliminar caracteres que no sean dígitos, punto o signo menos
        s = re.sub(r'[^0-9\.-]', '', s)
        return s

    for col in columns:
        # Aplicar la función de limpieza a cada valor
        df[col] = df[col].apply(clean_value)
        # Convertir a numérico, NaN si falla
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def main():
    # 1. Definir la ruta del archivo
    dataset_path = "/Users/mauriciosobarzo/Desktop/2025/Greensy/Lanzadera/TRIVO-LZAI3/final_dataset_with_score.csv"

    # 2. Cargar el CSV
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        sys.exit(f"Error: No se encontró el archivo en la ruta: {dataset_path}")

    print("Columnas del dataset:", df.columns.tolist())

    # 3. Seleccionar features y variable objetivo
    #    Asumimos que las columnas de proporciones comienzan con "porc_"
    #    y que la columna de score se llama "score_aceptacion".
    features_columns = [col for col in df.columns if col.startswith("porc_")]

    # Opcional: Agregar columnas nutricionales, si existen
    optional_nutrition = ["sodio_total", "calorias_totales"]
    features_columns += [col for col in optional_nutrition if col in df.columns]

    if not features_columns:
        sys.exit("Error: No se encontraron columnas de features ('porc_' o nutricionales).")

    score_col = "score_aceptacion"
    if score_col not in df.columns:
        sys.exit(f"Error: No se encontró la columna de score '{score_col}' en el dataset.")

    # 4. Preprocesar columnas numéricas (features + score)
    df = preprocess_numeric_columns(df, features_columns + [score_col])

    # 5. Verificar que todas las columnas sean numéricas
    for col in features_columns + [score_col]:
        if not pd.api.types.is_numeric_dtype(df[col]):
            print(f"Error: La columna '{col}' no es numérica tras preprocesamiento.")
            print("Valores únicos:", df[col].unique())
            sys.exit(1)

    # 6. Mostrar valores NaN (si los hay) para depurar
    for col in features_columns + [score_col]:
        if df[col].isna().any():
            nan_values = df.loc[df[col].isna(), col].unique()
            print(f"Valores no convertidos en '{col}':", nan_values)

    # 7. Eliminar filas con NaN
    initial_rows = df.shape[0]
    df.dropna(subset=features_columns + [score_col], inplace=True)
    dropped_rows = initial_rows - df.shape[0]
    if dropped_rows > 0:
        print(f"Advertencia: Se eliminaron {dropped_rows} filas por valores faltantes.")

    if df.empty:
        sys.exit("Error: No quedan filas después de eliminar valores faltantes. Revisa tus datos.")

    # 8. Dividir datos en entrenamiento (80%) y prueba (20%)
    x = df[features_columns]
    y = df[score_col]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    # 9. Definir un Pipeline con caché
    memory = joblib.Memory(location="./cachedir", verbose=0)
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor(random_state=42))
    ], memory=memory)

    # 10. Configurar GridSearchCV para optimizar hiperparámetros
    param_grid = {
        "model__n_estimators": [100, 200],
        "model__max_depth": [None, 10, 20],
        "model__min_samples_split": [2, 5]
    }

    grid_search = GridSearchCV(
        pipeline,
        param_grid,
        cv=5,
        scoring="neg_mean_squared_error",
        n_jobs=-1,
        error_score='raise'
    )

    # 11. Entrenar el modelo
    try:
        grid_search.fit(x_train, y_train)
    except Exception as e:
        sys.exit(f"Error durante el entrenamiento: {e}")

    # 12. Evaluar el modelo en el conjunto de prueba
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(x_test)
    r2 = r2_score(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)

    print("Mejor configuración de hiperparámetros:", grid_search.best_params_)
    print(f"R² en test: {r2:.4f}")
    print(f"RMSE en test: {rmse:.4f}")

    # 13. Guardar el modelo entrenado
    model_filename = "best_random_forest_model.pkl"
    joblib.dump(best_model, model_filename)
    print(f"Modelo guardado en '{model_filename}'")

if __name__ == "__main__":
    main()
