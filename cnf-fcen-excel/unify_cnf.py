#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

# 1. Cargar los archivos Excel
df_food_name = pd.read_excel("FOOD NAME.xlsx")
df_food_group = pd.read_excel("FOOD GROUP.xlsx")
df_nutrient_name = pd.read_excel("NUTRIENT NAME.xlsx")
df_nutrient_amount = pd.read_excel("NUTRIENT AMOUNT.xlsx")

# 2. Unir FoodName y FoodGroup
df_food = pd.merge(df_food_name, df_food_group, on="FoodGroupID", how="left")

# 3. Unir con NutrientAmount y NutrientName
df_food_nutrients = pd.merge(df_food, df_nutrient_amount, on="FoodID", how="left")
df_food_nutrients = pd.merge(df_food_nutrients, df_nutrient_name, on="NutrientID", how="left")

# 4. Mostrar columnas y valores únicos de NutrientName (para referencia)
print("Columnas de df_food_nutrients:", df_food_nutrients.columns)
unique_nutrients = df_food_nutrients["NutrientName"].unique()
print("\nValores únicos de NutrientName:", unique_nutrients)

# 5. Lista de nutrientes de interés (corregida para que coincida con tus datos)
wanted_nutrients = [
    "PROTEIN",
    "FAT (TOTAL LIPIDS)",
    "CARBOHYDRATE, TOTAL (BY DIFFERENCE)",
    "FIBRE, TOTAL DIETARY",
    "SODIUM",
    "ENERGY (KILOCALORIES)"
]

# 6. Filtrar
df_filtered = df_food_nutrients[df_food_nutrients["NutrientName"].isin(wanted_nutrients)]

print(f"\nTamaño de df_filtered tras filtrar: {len(df_filtered)}")
print("Columnas en df_filtered:", df_filtered.columns)
print("\nPrimeras filas de df_filtered:")
print(df_filtered.head(10))

# 7. Pivotar usando 'FoodDescription' en vez de 'FoodName'
try:
    df_pivot = df_filtered.pivot_table(
        index=["FoodID", "FoodDescription", "FoodGroupName"],
        columns="NutrientName",
        values="NutrientValue",
        aggfunc="mean"
    ).reset_index()

    # 8. Guardar a CSV
    df_pivot.to_csv("canadian_cnf_unified.csv", index=False)
    print("\nArchivo 'canadian_cnf_unified.csv' generado con éxito!")
except KeyError as e:
    print(f"\nERROR: No existe la columna {e} en df_filtered. "
          f"Revisa qué columnas hay y ajusta el 'index=['...']' del pivot_table.")
