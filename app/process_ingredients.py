import json
import os

# Listado de ingredientes clave extraídos del informe de CREAS
creas_ingredients = [
    'garbanzo_flour', 'olive_oil', 'water', 'salt', 'psyllium', 'rice_flour',
    'tapioca_starch', 'cornstarch', 'egg_white_powder', 'sunflower_oil'
]

# Cargar los datos de los archivos JSON en data/ingredients
ingredient_data_files = [
    '/Users/mauriciosobarzo/Desktop/2025/Greensy/Lanzadera/TRIVO-LZAI3/data/ingredients_data.json',
    '/Users/mauriciosobarzo/Desktop/2025/Greensy/Lanzadera/TRIVO-LZAI3/data/classified_ingredients.json'
]

# Función para cargar ingredientes de los archivos JSON
def load_ingredient_data(files):
    all_data = []
    for file in files:
        with open(file, 'r') as f:
            all_data.extend(json.load(f))
    return all_data

# Cargar todos los ingredientes de los archivos JSON
ingredient_data = load_ingredient_data(ingredient_data_files)

# Normalizar los ingredientes encontrados y seleccionados
normalized_ingredients = []
for ingredient in ingredient_data:
    ingredient_name = ingredient['ingredient'].lower().replace(' ', '_')
    if ingredient_name in creas_ingredients:
        normalized_ingredient = {
            'ingredient': ingredient_name,
            'type': ingredient['type'],
            'nutritional_values': {
                'sodium': ingredient['nutritional_values'].get('sodium', 0),
                'fiber': ingredient['nutritional_values'].get('fiber', 0),
                'protein': ingredient['nutritional_values'].get('protein', 0)
            }
        }
        normalized_ingredients.append(normalized_ingredient)

# Crear la carpeta 'processed_ingredients' si no existe
output_folder = '/Users/mauriciosobarzo/Desktop/2025/Greensy/Lanzadera/TRIVO-LZAI3/data/processed_ingredients'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Guardar los datos procesados en un archivo JSON en la carpeta creada
output_file = os.path.join(output_folder, 'processed_ingredients.json')
with open(output_file, 'w') as f:
    json.dump(normalized_ingredients, f, indent=4)

print(f'Datos normalizados y guardados en {output_file}')
