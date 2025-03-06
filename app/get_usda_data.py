
import requests
import json

# Función para obtener datos nutricionales de la API de USDA
def get_usda_data(ingredient_name, api_key):
    url = f'https://api.nal.usda.gov/fdc/v1/foods/search?query={ingredient_name}&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f'Respuesta completa para {ingredient_name}: {json.dumps(data, indent=4)}')  # Imprimir toda la respuesta
        if data['foods']:
            food = data['foods'][0]  # Tomamos el primer resultado
            nutritional_values = {
                'sodium': food['foodNutrients'][0]['value'],  # Asumimos que el sodio está en la primera posición
                'fiber': food['foodNutrients'][1]['value'],   # Asumimos que la fibra está en la segunda posición
                'protein': food['foodNutrients'][2]['value']  # Asumimos que la proteína está en la tercera posición
            }
            return nutritional_values
    return None

# Lista de ingredientes de Greensy
ingredients = ['garbanzo flour', 'olive oil', 'water', 'salt']
api_key = 'Rntzc9HDaefGgZL0w3Sid120qfk4kdJD4YZuicE4'  # Tu clave API de USDA

# Recopilar datos para cada ingrediente
ingredients_data = []
for ingredient in ingredients:
    data = get_usda_data(ingredient, api_key)
    if data:
        ingredients_data.append({
            'ingredient': ingredient,
            'type': 'vegetal' if ingredient != 'salt' else 'mineral',  # Se clasifica el tipo de ingrediente
            'nutritional_values': data
        })

# Mostrar los resultados en la terminal
print(json.dumps(ingredients_data, indent=4))

