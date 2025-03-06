import json
import re

def extract_quantity(line_text):
    match = re.search(r'(\d+)\s*g', line_text.lower())
    if match:
        return int(match.group(1))
    return None

def unify_data(filtered_lines, ingredients_info):
    results = []
    for entry in filtered_lines:
        text_lower = entry['text'].lower()
        page = entry['page']

        for ingredient_key, info in ingredients_info.items():
            # Convertimos 'harina_de_garbanzo' a un patrón 'harina\s+de\s+garbanzo'
            name_for_search = ingredient_key.replace('_', r'\s+')

            if re.search(name_for_search, text_lower):
                quantity = extract_quantity(text_lower)
                results.append({
                    'ingredient': ingredient_key,
                    'function': info.get('funcion'),
                    'cost_kg': info.get('costo_kg'),
                    'line_text': entry['text'],
                    'page': page,
                    'quantity_g': quantity
                })
                break
    return results

def main():
    with open('filtered_data.json', 'r') as f:
        filtered_lines = json.load(f)

    with open('ingredients_info.json', 'r') as f:
        ingredients_info = json.load(f)

    final_data = unify_data(filtered_lines, ingredients_info)

    with open('normalized_data.json', 'w') as f:
        json.dump(final_data, f, indent=4)

    print(f'Normalizacion completada. Se han generado {len(final_data)} entradas en normalized_data.json')

if __name__ == '__main__':
    main()

