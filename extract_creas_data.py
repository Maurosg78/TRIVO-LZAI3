#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pdfplumber

def extract_creas_data(pdf_path):
    """
    Ejemplo de lectura de un PDF de CREAS con pdfplumber.
    Extrae texto y tablas de cada página y los imprime.
    """
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            # Extraer texto de la página
            text = page.extract_text()
            print(f"\n=== Página {page_number+1} - TEXTO ===")
            print(text)

            # Extraer tablas
            tables = page.extract_tables()
            for idx, table in enumerate(tables):
                print(f"\n--- Tabla {idx+1} en página {page_number+1} ---")
                for row in table:
                    print(row)

if __name__ == "__main__":
    # Ajusta la ruta a tu PDF de CREAS
    pdf_path = "data/pdfs/20CV-152107 - INFORME TÉCNICO CREAS - GREENS SPA.pdf"

