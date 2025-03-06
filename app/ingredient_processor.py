import json
import requests

def load_ingredients():
    with open('data/ingredients_data.json', 'r') as f:
        return json.load(f)

def fetch_ingredients_data():
    ingredients = load_ingredients()
    for ingredient in ingredients:
        # Suponiendo que 'ingredient' tiene una clave 'name'
        response = requests.get(f'https://api.spoonacular.com/food/ingredients/{ingredient["name"]}')
        ingredient['data'] = response.json()

    with open('data/processed_ingredients.json', 'w') as f:
        json.dump(ingredients, f, indent=4)

if __name__ == "__main__":
    fetch_ingredients_data()
