import requests
import json

# Cargar las claves de la API desde el archivo de configuración
def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

config = load_config()

SPOONACULAR_API_KEY = config.get('spoonacular_api_key')

# Función para obtener los ingredientes de Spoonacular
def get_ingredients_from_spoonacular(query):
    url = f"https://api.spoonacular.com/food/ingredients/search?query={query}&apiKey={SPOONACULAR_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al hacer la solicitud a la API de Spoonacular: {response.status_code}")
        return None

# Procesar y guardar los ingredientes
def process_ingredients(ingredients_data):
    if not ingredients_data:
        print("No hay datos para procesar.")
        return

    ingredients = ingredients_data.get('results', [])
    saved_ingredients = []

    for ingredient in ingredients:
        name = ingredient['name']
        image = ingredient.get('image', '')
        ingredient_id = ingredient['id']
        
        # Guardar el ingrediente (puedes guardarlo en una base de datos o archivo, por ahora solo lo mostramos)
        saved_ingredients.append({
            'id': ingredient_id,
            'name': name,
            'image': image
        })
        
    print(f"Procesados y guardados {len(saved_ingredients)} ingredientes.")
    return saved_ingredients

# Ejemplo de consulta a la API para tomates
ingredients_data = get_ingredients_from_spoonacular("tomato")
saved_ingredients = process_ingredients(ingredients_data)
