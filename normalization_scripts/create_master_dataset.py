#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os

def create_master_dataset():
    """
    Este script lee los CSV normalizados de cada fuente (Canadá, Ciqual, USDA, etc.)
    y los concatena en un solo archivo 'master_dataset_full.csv'.
    Ajusta las rutas y nombres de archivo según tu caso.
    """
    
    # Ajusta las rutas según donde tengas cada CSV unificado
    # Ejemplos (modifica si tus archivos están en otra carpeta):
    ciqual_csv = "ciqual_unified.csv"
    cnf_csv = "canadian_cnf_unified.csv"
    usda_csv = "usda_unified.csv"


    # Creamos una lista para DataFrames
    dfs = []

    # 1. Cargar Ciqual si existe
    if os.path.isfile(ciqual_csv):
        df_ciqual = pd.read_csv(ciqual_csv)
        dfs.append(df_ciqual)
        print(f"Leído: {ciqual_csv} con {len(df_ciqual)} filas.")
    else:
        print(f"No se encontró {ciqual_csv}. Saltando...")

    # 2. Cargar CNF (Canadá) si existe
    if os.path.isfile(cnf_csv):
        df_cnf = pd.read_csv(cnf_csv)
        dfs.append(df_cnf)
        print(f"Leído: {cnf_csv} con {len(df_cnf)} filas.")
    else:
        print(f"No se encontró {cnf_csv}. Saltando...")

    # 3. Cargar USDA si existe
    if os.path.isfile(usda_csv):
        df_usda = pd.read_csv(usda_csv)
        dfs.append(df_usda)
        print(f"Leído: {usda_csv} con {len(df_usda)} filas.")
    else:
        print(f"No se encontró {usda_csv}. Saltando...")

    # Si tenemos al menos un DataFrame
    if len(dfs) > 0:
        # Unimos con outer concat para no perder columnas
        df_master = pd.concat(dfs, ignore_index=True, sort=False)

        # Exportamos
        output_file = "master_dataset_full.csv"
        df_master.to_csv(output_file, index=False, encoding="utf-8")
        print(f"\nArchivo maestro '{output_file}' generado con {len(df_master)} filas.")
    else:
        print("No se cargó ningún CSV. Revisa rutas y nombres de archivo.")

if __name__ == "__main__":
    create_master_dataset()
