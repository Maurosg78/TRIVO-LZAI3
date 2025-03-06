import os
import json
import re

# Mapeo de nombres de nutrientes USDA -> nombres internos
NUTRIENT_MAP = {
    'Protein': 'protein',
    'Carbohydrate, by difference': 'carbs',
    'Total lipid (fat)': 'fat',
    'Fiber, total dietary': 'fiber',
    'Sodium, Na': 'sodium',
    'Energy': 'energy'
}

def parse_food_nutrients(food_nutrients):
    """Dado el array foodNutrients de USDA, extrae los valores clave."""
    normalized = {
        'protein': 0,
        'carbs': 0,
        'fat': 0,
        'fiber': 0,
        'sodium': 0,
        'energy': 0
    }
    for fn in food_nutrients:
        nutrient_name = fn.get('nutrientName')
        value = fn.get('value', 0)
        if nutrient_name in NUTRIENT_MAP:
            normalized_key = NUTRIENT_MAP[nutrient_name]
            normalized[normalized_key] = value
    return normalized

def normalize_usda_item(item):
    """Normaliza un dict con la estructura USDA (Branded o SR Legacy)."""
    # Muchos archivos tienen 'description' como nombre
    ingredient_name = item.get('description', '').lower().replace(' ', '_')

    # Si el archivo tiene 'foodNutrients', lo parseamos
    food_nutrients = item.get('foodNutrients', [])
    # A veces puede estar en un array "foods" si es FDC search result
    if isinstance(item.get('foods'), list) and item['foods']:
        # Tomamos el primer "food" o iteramos todos
        first_food = item['foods'][0]
        ingredient_name = first_food.get('description', ingredient_name).lower().replace(' ', '_')
        food_nutrients = first_food.get('foodNutrients', [])

    nutrients = parse_food_nutrients(food_nutrients)

    return {
        'ingredient_name': ingredient_name,
        'type': 'usda',
        'nutritional_values': nutrients
    }

def main():
    ingredients_folder = '/Users/mauriciosobarzo/Desktop/2025/Greensy/Lanzadera/TRIVO-LZAI3/data/ingredients'
    all_normalized = []

    for filename in os.listdir(ingredients_folder):
        if filename.endswith('.json'):
            filepath = os.path.join(ingredients_folder, filename)
            with open(filepath, 'r') as f:
                try:
                    data = json.load(f)

                    # data puede ser dict o lista
                    if isinstance(data, dict):
                        # Caso: un solo item USDA
                        normalized_item = normalize_usda_item(data)
                        if normalized_item['ingredient_name']:
                            all_normalized.append(normalized_item)
                    elif isinstance(data, list):
                        # Caso: varios items en una lista
                        for item in data:
                            normalized_item = normalize_usda_item(item)
                            if normalized_item['ingredient_name']:
                                all_normalized.append(normalized_item)
                except json.JSONDecodeError:
                    print(f'Archivo {filename} no es un JSON válido. Se omite.')

    output_path = '/Users/mauriciosobarzo/Desktop/2025/Greensy/Lanzadera/TRIVO-LZAI3/data/normalized_usda_data.json'
    with open(output_path, 'w') as out:
        json.dump(all_normalized, out, indent=4)

    print(f'Proceso completado. Se han normalizado {len(all_normalized)} ingredientes en {output_path}')

if __name__ == '__main__':
    main()

