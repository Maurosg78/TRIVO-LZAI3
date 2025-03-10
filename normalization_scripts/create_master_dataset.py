#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script ejemplo para unificar datos (Ciqual, CNF, USDA, etc.)
y generar un 'final_dataset.csv' que usaremos en pipeline.py
"""

import pandas as pd
import os

def create_master_dataset():
    # Rutas (ajusta según tu caso real)
    ciqual_path = "ciqual_unified.csv"
    cnf_path = "canadian_cnf_unified.csv"
    usda_path = "usda_unified.csv"
    output_file = "final_dataset.csv"

    # Lee cada CSV si existe
    df_ciqual = pd.read_csv(ciqual_path) if os.path.exists(ciqual_path) else pd.DataFrame()
    df_cnf = pd.read_csv(cnf_path) if os.path.exists(cnf_path) else pd.DataFrame()
    df_usda = pd.read_csv(usda_path) if os.path.exists(usda_path) else pd.DataFrame()

    # Pequeño renombrado genérico (ajusta a tu gusto)
    rename_map = {
        "Protein (g/100g)": "protein_g",
        "Fat (g/100g)": "fat_g",
        "Carbohydrate (g/100g)": "carbs_g",
        "Fibres (g/100g)": "fiber_g",
        "Sodium (mg/100g)": "sodium_mg",
        "Energy_kcal_100g": "energy_kcal",
    }

    def unify_columns(df):
        return df.rename(columns=rename_map)

    df_ciqual = unify_columns(df_ciqual)
    df_cnf = unify_columns(df_cnf)
    df_usda = unify_columns(df_usda)

    # Concatenar
    df_nutrients = pd.concat([df_ciqual, df_cnf, df_usda], ignore_index=True)

    # Quita filas totalmente vacías
    df_nutrients.dropna(how="all", inplace=True)

    # (Opcional) Podrías unir con datos de "extended_ingredients_info.json" o CREAS, etc.

    # Guardar CSV unificado
    df_nutrients.to_csv(output_file, index=False, encoding="utf-8")
    print(f"[OK] Archivo '{output_file}' generado con {len(df_nutrients)} filas.")

if __name__ == "__main__":
    create_master_dataset()
