#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import pandas as pd

def normalize_usda_json():
    # Ajusta la ruta de tu JSON
    input_file = "data/normalized_usda_data.json"
    # Nombre de archivo CSV de salida
    output_file = "usda_unified.csv"

    # Si el CSV ya existe, pedimos confirmación para sobrescribir
    if os.path.exists(output_file):
        resp = input(f"El archivo '{output_file}' ya existe. ¿Sobrescribir? (s/n): ")
        if resp.lower() != "s":
            print("Operación cancelada. No se generó un nuevo CSV.")
            return

    # Cargar el JSON
    if not os.path.exists(input_file):
        print(f"No se encontró el archivo JSON: {input_file}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"El JSON '{input_file}' no es una lista de ingredientes.")
        return

    # data es una lista de dicts con estructura:
    # [
    #   {
    #     "ingredient_name": "...",
    #     "type": "usda",
    #     "nutritional_values": {
    #       "protein": ...,
    #       "carbs": ...,
    #       "fat": ...,
    #       "fiber": ...,
    #       "sodium": ...,
    #       "energy": ...
    #     }
    #   },
    #   ...
    # ]

    rows = []
    for item in data:
        ing_name = item.get("ingredient_name", "Unknown")
        nutri = item.get("nutritional_values", {})
        # Creamos una fila con columnas estandarizadas
        row = {
            "source": "USDA",  # Fijamos la fuente
            "FoodID": ing_name,
            "FoodName": ing_name,
            # Ajusta el nombre de las columnas según tu convención
            "Protein_g_100g": nutri.get("protein", None),
            "Fat_g_100g": nutri.get("fat", None),
            "Carbs_g_100g": nutri.get("carbs", None),
            "Fiber_g_100g": nutri.get("fiber", None),
            "Sodium_mg_100g": nutri.get("sodium", None),
            "Energy_kcal_100g": nutri.get("energy", None)
        }
        rows.append(row)

    # Convertimos la lista de filas en un DataFrame
    df_usda = pd.DataFrame(rows)
    print(f"Se han procesado {len(df_usda)} ingredientes de USDA.")

    # Guardar en CSV
    df_usda.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Archivo '{output_file}' generado con éxito!")

if __name__ == "__main__":
    normalize_usda_json()
