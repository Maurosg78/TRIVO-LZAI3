#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob

def parse_creas_texts(folder="data/pdfs"):
    """
    Ejemplo simple que:
    - Lee todos los .txt en data/pdfs/
    - Busca líneas que contengan 'Tabla'
    - Guarda esas líneas en 'creas_tables.csv'
    """
    txt_files = glob.glob(os.path.join(folder, "*.txt"))
    output_file = "creas_tables.csv"

    with open(output_file, "w", encoding="utf-8") as out:
        # Escribimos encabezado CSV
        out.write("archivo, linea\n")

        for txt_path in txt_files:
            base_name = os.path.basename(txt_path)
            with open(txt_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines:
                # Ejemplo: si la línea contiene la palabra 'Tabla'
                if "Tabla" in line:
                    # Reemplazamos comas por puntoycoma para no romper CSV
                    safe_line = line.strip().replace(",", ";")
                    out.write(f"{base_name},{safe_line}\n")

    print(f"[DONE] Se ha creado '{output_file}' con líneas que contienen 'Tabla'.")

if __name__ == "__main__":
    parse_creas_texts()
