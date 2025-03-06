import json
import requests

def load_ingredients_data():
    with open('data/ingredients_data.json', 'r') as f:
        return json.load(f)

def classify_ingredient(ingredient):
    if ingredient['type'] == 'vegetal':
        return 'Vegetal'
    elif ingredient['type'] == 'animal':
        return 'Animal'
    else:
        return 'Desconocido'

def process_ingredients():
    data = load_ingredients_data()
    print(f"Datos cargados: {data}")  # Verifica qué datos se están cargando
    classified_ingredients = []

    for ingredient in data:
        classification = classify_ingredient(ingredient)
        ingredient['classification'] = classification
        classified_ingredients.append(ingredient)

    with open('data/classified_ingredients.json', 'w') as f:
        json.dump(classified_ingredients, f, indent=4)
    return classified_ingredients


if __name__ == "__main__":
    process_ingredients()
