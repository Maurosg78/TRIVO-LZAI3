#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

# Ruta al archivo de Ciqual (ajusta si es distinta)
FILE_PATH = "../Table Ciqual 2020_ENG_2020 07 07.xls"

def normalize_ciqual():
    df = pd.read_excel(FILE_PATH)
    
    # Imprime columnas originales
    print("Columnas originales en Ciqual:", df.columns.tolist())

    # Aquí definimos un renombrado genérico (ajusta según desees)
    # Asumiendo que existen columnas como "alim_code", "alim_nom_eng", etc.
    rename_map = {
        "alim_code": "FoodID",
        "alim_nom_eng": "FoodName",
        "Energy, Regulation EU No 1169/2011 (kcal/100g)": "Energy_kcal_100g",
        "Protein (g/100g)": "Protein_g_100g",
        "Fat (g/100g)": "Fat_g_100g",
        "Carbohydrate (g/100g)": "Carbs_g_100g",
        "Fibres (g/100g)": "Fiber_g_100g",
        "Salt (g/100g)": "Salt_g_100g",
        "Sodium (mg/100g)": "Sodium_mg_100g",
        # Agrega más si quieres
    }
    
    # Crear una lista con todas las columnas (no descartamos nada),
    # solo renombramos las que conocemos.
    # El resto quedarán con su nombre original.
    df_renamed = df.rename(columns=rename_map)
    
    # Agregamos columna "source" para saber de dónde viene
    df_renamed["source"] = "Ciqual"

    # Guardar CSV con todo, pero renombrado parcialmente
    output_file = "ciqual_unified.csv"
    df_renamed.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Archivo '{output_file}' generado con éxito!")

if __name__ == "__main__":
    normalize_ciqual()
