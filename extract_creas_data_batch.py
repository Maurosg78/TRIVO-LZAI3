#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob

# Escoge UNO de estos métodos:
# 1) pdfplumber (si el PDF tiene texto embebido)
import pdfplumber

# 2) pdf2image + pytesseract (si el PDF es un escaneo)
# from pdf2image import convert_from_path
# import pytesseract

def extract_text_pdfplumber(pdf_path):
    """
    Extrae texto de un PDF con pdfplumber y retorna un string.
    """
    text_result = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            text = page.extract_text()
            text_result.append(f"=== Página {page_number+1} ===\n{text}\n")
    return "\n".join(text_result)

# Si tu PDF es un escaneo, usarías en cambio algo como:
"""
def extract_text_ocr(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    text_result = []
    for i, page_img in enumerate(pages):
        text = pytesseract.image_to_string(page_img, lang="spa")
        text_result.append(f"=== Página {i+1} ===\n{text}\n")
    return "\n".join(text_result)
"""

def main():
    pdf_folder = "data/pdfs/"
    pdf_files = glob.glob(os.path.join(pdf_folder, "*.pdf"))

    for pdf_path in pdf_files:
        # Generar nombre de salida .txt
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        txt_path = os.path.join(pdf_folder, base_name + ".txt")

        # Verificar si el .txt existe
        if os.path.exists(txt_path):
            print(f"[SKIP] Ya existe {txt_path}, no se extrae de nuevo.")
        else:
            print(f"[EXTRACT] Leyendo {pdf_path}...")
            # Extraer con pdfplumber (o con OCR, según tu caso)
            extracted_text = extract_text_pdfplumber(pdf_path)
            # Guardar el texto en el .txt
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            print(f"[DONE] Texto guardado en {txt_path}")

if __name__ == "__main__":
    main()
