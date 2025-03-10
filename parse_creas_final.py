#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import unicodedata
import csv
from typing import List, Tuple, Optional

def normalize_str(s: str) -> str:
    """
    Normaliza una cadena quitando tildes/diacríticos y convirtiendo a minúsculas.
    
    Args:
        s (str): Cadena a normalizar.
    Returns:
        str: Cadena normalizada.
    """
    s = s.lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

def normalize_percentage(percentage: str) -> str:
    """
    Normaliza un porcentaje reemplazando separadores y eliminando el símbolo %.
    
    Args:
        percentage (str): Cadena con el porcentaje (e.g., "32;3%", "32,3%").
    Returns:
        str: Porcentaje normalizado (e.g., "32.3").
    """
    cleaned = percentage.replace(";", ".").replace(",", ".").replace("%", "")
    parts = cleaned.split(".")
    if len(parts) > 2:
        return ".".join(parts[-2:])
    return cleaned

def extract_ingredient_percentage(entry: str) -> Optional[Tuple[str, str]]:
    """
    Extrae el ingrediente y el porcentaje de una entrada.
    
    Args:
        entry (str): Cadena a analizar (e.g., "Harina de arroz 32;3%").
    Returns:
        Optional[Tuple[str, str]]: Tupla con (ingrediente, porcentaje) o None si no hay coincidencia.
    """
    regex = re.compile(r"(.*?)\s+([\d,;\.]+%)$")
    match = regex.search(entry.strip())
    if match:
        ingrediente = match.group(1).strip()
        porcentaje = normalize_percentage(match.group(2))
        return ingrediente, porcentaje
    return None

def parse_table_details(
    input_file: str,
    output_file: str,
    table_identifier: str,
    formulation_keyword: str,
    delimiter: str = ";"
) -> None:
    """
    Parsea un archivo CSV para extraer ingredientes y porcentajes de una tabla específica.
    
    Args:
        input_file (str): Ruta del archivo de entrada.
        output_file (str): Ruta del archivo de salida.
        table_identifier (str): Identificador de la tabla (e.g., "tabla 3.2").
        formulation_keyword (str): Palabra clave para identificar la formulación.
        delimiter (str): Delimitador usado en col2 para separar entradas.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    results: List[Tuple[str, str]] = []
    found_table = False

    for line in lines:
        if line.startswith("tabla_id,contenido"):
            continue

        parts = line.strip().split(",", 1)
        if len(parts) < 2:
            continue

        col1, col2 = parts[0].strip(), parts[1].strip()
        col1_norm = normalize_str(col1)

        if not found_table:
            if table_identifier in col1_norm and formulation_keyword in col1_norm:
                found_table = True
                entries = col2.split(delimiter)
                for entry in entries:
                    result = extract_ingredient_percentage(entry)
                    if result:
                        results.append(result)
                continue
        else:
            if table_identifier not in col1_norm:
                break
            entries = col2.split(delimiter)
            for entry in entries:
                result = extract_ingredient_percentage(entry)
                if result:
                    results.append(result)

    with open(output_file, "w", encoding="utf-8", newline='') as out:
        writer = csv.writer(out)
        writer.writerow(["Ingrediente", "Porcentaje"])
        for ingrediente, porcentaje in results:
            ingrediente_safe = ingrediente.replace(",", " ")
            writer.writerow([ingrediente_safe, porcentaje])

    print(f"[DONE] Se ha creado '{output_file}' con la formulación final ({table_identifier}).")

if __name__ == "__main__":
    parse_table_details(
        input_file="creas_tables_details.csv",
        output_file="final_formulation.csv",
        table_identifier="tabla 3.2",
        formulation_keyword="formulacion",
        delimiter=";"
    )
