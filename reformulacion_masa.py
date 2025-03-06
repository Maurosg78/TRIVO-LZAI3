#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas as pd

########################################
# 1. LECTURA DE ARCHIVOS JSON
########################################

allowed_categories = {
    'harina', 'almidon', 'aceite', 'goma',
    'fibra', 'vegetal', 'semilla', 'sal_mineral',
    'agente_leudante', 'agente_fermentador'
}

# Cargar extended_ingredients_info.json
with open('extended_ingredients_info.json', 'r', encoding='utf-8') as f:
    extended_info = json.load(f)

# Filtrar ingredientes que estén en las categorías permitidas
filtered_ingredients = {
    name: data
    for name, data in extended_info.items()
    if data['categoria'] in allowed_categories
}

print('Ingredientes vegetales/naturales permitidos:')
for ing_name, ing_data in filtered_ingredients.items():
    print(f" - {ing_name} | {ing_data['categoria']}")


# Cargar normalized_usda_data.json (nutrición)
with open('data/normalized_usda_data.json', 'r', encoding='utf-8') as f:
    usda_data = json.load(f)

# Convertir a DataFrame para búsquedas más cómodas
usda_df = pd.DataFrame(usda_data)
usda_df.set_index('ingredient_name', inplace=True)

print('\\nEjemplo de DataFrame USDA (primeras filas):')
print(usda_df.head())

########################################
# 2. EJEMPLO DE FORMULACIÓN DE MASA
########################################

# Masa A (100 g totales) - ejemplo
masa_A = [
    {'name': 'harina_de_garbanzo',    'amount_g': 50},
    {'name': 'almidon_de_tapioca',   'amount_g': 30},
    {'name': 'goma_xantana',         'amount_g': 1},
    {'name': 'levadura_deshidratada','amount_g': 2},
    {'name': 'salt',                 'amount_g': 0.5},  # Sal normal
    {'name': 'cloruro_de_potasio',   'amount_g': 0.5},  # Sustituto sal
    {'name': 'aceite_de_oliva',      'amount_g': 3},
    {'name': 'water',                'amount_g': 13}
]

print('\\n=== Cálculo de costo y sodio para la Masa A (100 g) ===')

total_cost = 0.0
total_sodio_mg = 0.0
total_gramos = sum(ing['amount_g'] for ing in masa_A)

for ing in masa_A:
    ing_name = ing['name']
    ing_g    = ing['amount_g']

    # 2.1 Calcular costo
    if ing_name in filtered_ingredients:
        cost_kg = filtered_ingredients[ing_name]['cost_kg']
    else:
        cost_kg = 0.0

    cost_ing = (ing_g / 1000.0) * cost_kg
    total_cost += cost_ing

    # 2.2 Calcular sodio
    if ing_name == 'salt':
        sodium_per_100g = 39300.0  # mg/100g
    elif ing_name == 'cloruro_de_potasio':
        sodium_per_100g = 0.0
    else:
        if ing_name in usda_df.index:
            sodium_per_100g = usda_df.loc[ing_name, 'nutritional_values']['sodium']
        else:
            sodium_per_100g = 0.0

    ing_sodium_mg = (ing_g / 100.0) * sodium_per_100g
    total_sodio_mg += ing_sodium_mg

sodio_por_100g = (total_sodio_mg / total_gramos) * 100

print(f'Costo total de la masa (100 g): {total_cost:.3f} €')
print(f'Sodio total (mg) por 100 g de masa: {sodio_por_100g:.1f} mg')

########################################
# 3. CONCLUSIÓN
########################################

print('\\nScript finalizado. Puedes ajustar cantidades, sustituir ingredientes,')
print('y/o crear combinaciones dinámicas con heurísticas o redes neuronales.')
