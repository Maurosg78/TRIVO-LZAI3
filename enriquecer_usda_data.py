#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import time

# IMPORTANTE:
# Asegúrate de que 'get_usda_data.py' esté en la misma carpeta o ajusta la importación.
# O bien, podemos copiar la lógica de fetch_usda_data directamente aquí.

# Para simplicidad, incluimos una versión local de fetch_usda_data:
API_KEY = "Rntzc9HDaefGgZL0w3Sid120qfk4kdJD4YZuicE4"  # Tu API key
BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

def fetch_usda_data(query, page_size=1):
    params = {
        "query": query,
        "pageSize": page_size,
        "dataType": ["Foundation", "SR Legacy", "Branded"],
        "api_key": API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con USDA para '{query}': {e}")
        return None

##############################################
# 1. Leer extended_ingredients_info.json
##############################################

# Ajusta la ruta si tu JSON está en otro lugar
EXTENDED_INFO_FILE = "extended_ingredients_info.json"
with open(EXTENDED_INFO_FILE, "r", encoding="utf-8") as f:
    extended_info = json.load(f)

##############################################
# 2. Mapeo español -> inglés para USDA
##############################################
# Añade las traducciones que necesites.
# Clave: nombre en español (coincide con extended_info)
# Valor: query en inglés para USDA
mapping_es_en = {
    "harina_de_garbanzo": "chickpea flour",
    "harina_de_arroz": "rice flour",
    "harina_de_arroz_integral": "brown rice flour",
    "almidon_de_maiz": "cornstarch",
    "almidon_de_mandioca": "manioc starch",
    "almidon_de_tapioca": "tapioca starch",
    "almidon_de_papa": "potato flour",
    "goma_xantana": "xanthan gum",
    "bicarbonato_de_sodio": "sodium bicarbonate",
    "levadura_deshidratada": "yeast",
    "cloruro_de_potasio": "potassium chloride",
    "coliflor": "cauliflower",
    "papa": "potato",
    "espinaca": "spinach",
    "linaza_molida": "ground flaxseed",
    "aceite_de_oliva": "olive oil",
    # ... añade más si lo deseas ...
}

##############################################
# 3. Nutrientes de interés
##############################################
# Lista de nutrientNames que queremos extraer del JSON de USDA
nutrients_of_interest = {
    "Protein": "protein",
    "Total lipid (fat)": "fat",
    "Carbohydrate, by difference": "carbs",
    "Fiber, total dietary": "fiber",
    "Sodium, Na": "sodium",
    "Energy": "calories",   # Kcal
    "Calcium, Ca": "calcium",
    "Iron, Fe": "iron",
    "Sugars, added": "sugars_added",
    "Total Sugars": "sugars_total",
    # Puedes añadir más según tus necesidades
}

##############################################
# 4. Función para extraer nutrientes relevantes
##############################################
def extract_nutrients_from_usda_data(usda_json):
    """
    usda_json: Respuesta completa de la API de USDA para 1 ingrediente.
    Devuelve un diccionario con los nutrientes de interés.
    """
    result = {key: 0.0 for key in nutrients_of_interest.values()}  # inicia en 0
    if not usda_json or "foods" not in usda_json:
        return result

    # Tomamos el primer 'food' de la lista, asumiendo el más relevante
    foods = usda_json.get("foods", [])
    if not foods:
        return result

    first_food = foods[0]
    food_nutrients = first_food.get("foodNutrients", [])

    for fn in food_nutrients:
        nutrient_name = fn.get("nutrientName", "")
        value = fn.get("value", 0.0)
        # Si coincide con uno de los nutrients_of_interest, lo guardamos
        if nutrient_name in nutrients_of_interest:
            key = nutrients_of_interest[nutrient_name]  # p.ej. "Protein" -> "protein"
            result[key] = value

    return result

##############################################
# 5. Crear nuevo diccionario unificado
##############################################
enriched_data = {}

for ing_name, ing_data in extended_info.items():
    # 5.1 Revisamos si ing_name está en el mapeo
    if ing_name not in mapping_es_en:
        # Si no tenemos traducción, podemos omitirlo o guardarlo tal cual
        print(f"No tenemos mapeo para '{ing_name}'. Se omite.")
        continue

    english_query = mapping_es_en[ing_name]
    print(f"Buscando en USDA -> {ing_name} ({english_query})")

    # 5.2 Llamamos a la API de USDA
    usda_json = fetch_usda_data(english_query, page_size=1)
    # Dormimos un poco para no saturar la API (opcional)
    time.sleep(0.5)

    # 5.3 Extraemos nutrientes
    nutrients_dict = extract_nutrients_from_usda_data(usda_json)

    # 5.4 Unimos con la data local
    enriched_data[ing_name] = {
        "categoria": ing_data["categoria"],
        "funcion": ing_data["funcion"],
        "cost_kg": ing_data["cost_kg"],
        "nutrients": nutrients_dict
    }

##############################################
# 6. Guardar el resultado en enriched_data.json
##############################################
OUTPUT_FILE = "enriched_data.json"
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(enriched_data, f, indent=2, ensure_ascii=False)

print(f"\nArchivo '{OUTPUT_FILE}' generado con éxito.")
