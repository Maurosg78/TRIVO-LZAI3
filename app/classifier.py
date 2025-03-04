import json
import requests
from sklearn.ensemble import RandomForestClassifier

# Cargar las claves de la API desde el archivo de configuración
def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

config = load_config()
SPOONACULAR_API_KEY = config.get('spoonacular_api_key')

# Función de ejemplo para clasificar ingredientes
def classify_ingredient(ingredient_name):
    # Aquí implementamos una clasificación básica usando un modelo de ejemplo
    # Este es solo un placeholder y puede ser reemplazado por un modelo más avanzado
    if ingredient_name.lower() == "tomato":
        return {"gluten_free": True, "vegan": True, "allergens": []}
    else:
        return {"gluten_free": False, "vegan": False, "allergens": ["None"]}

# Función para obtener detalles del ingrediente desde la API de Spoonacular
def get_ingredient_details(ingredient_id):
    url = f"https://api.spoonacular.com/food/ingredients/{ingredient_id}/information?apiKey={SPOONACULAR_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener detalles del ingrediente: {response.status_code}")
        return None

# Clasificación de ingredientes desde datos obtenidos de las APIs
def process_and_classify_ingredients(ingredients_data):
    classified_ingredients = []
    
    # Aquí tomamos los resultados de Spoonacular o USDA y los procesamos
    if 'results' in ingredients_data:
        for ingredient in ingredients_data['results']:
            ingredient_name = ingredient['name']
            ingredient_id = ingredient['id']
            classified_data = classify_ingredient(ingredient_name)
            
            ingredient_info = {
                "name": ingredient_name,
                "id": ingredient_id,
                "classification": classified_data
            }
            
            classified_ingredients.append(ingredient_info)
    
    return classified_ingredients

# Ejecutar la función de clasificación
if __name__ == "__main__":
    # Cargar datos de los ingredientes
    with open('ingredients_data.json', 'r') as f:
        ingredients_data = json.load(f)
    
    classified_ingredients = process_and_classify_ingredients(ingredients_data)
    
    # Guardar los ingredientes clasificados
    with open('classified_ingredients.json', 'w') as f:
        json.dump(classified_ingredients, f, indent=4)
    
    print(f"Clasificados y guardados {len(classified_ingredients)} ingredientes.")
