import json

# Función para cargar datos de los ingredientes

def load_ingredients_data(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

# Función para convertir los nombres de ingredientes en formato estándar (lowercase y guiones bajos)

def normalize_ingredient_names(ingredients):
    return [ing.lower().replace(' ', '_') for ing in ingredients]
