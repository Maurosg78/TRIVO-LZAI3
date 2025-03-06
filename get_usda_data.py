#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys

# Tu API key de USDA
API_KEY = 'Rntzc9HDaefGgZL0w3Sid120qfk4kdJD4YZuicE4'

# Endpoint base de USDA (FoodData Central)
BASE_URL = 'https://api.nal.usda.gov/fdc/v1/foods/search'

def fetch_usda_data(query, page_size=1):
    params = {
        'query': query,
        'pageSize': page_size,
        'dataType': ['Foundation', 'SR Legacy', 'Branded'],
        'api_key': API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Lanza error si status != 200
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error al conectar con USDA: {e}')
        return None

def main():
    if len(sys.argv) < 2:
        print('Uso: python get_usda_data.py <ingrediente> [page_size]')
        sys.exit(1)
    query = sys.argv[1]
    page_size = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    data = fetch_usda_data(query, page_size)
    if data:
        # Muestra resultados en pantalla (JSON pretty-print)
        print(json.dumps(data, indent=2))
    else:
        print('No se pudo obtener datos de USDA.')

if __name__ == '__main__':
    main()
