#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytesseract
from pdf2image import convert_from_path

def extract_text_via_ocr(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    for i, page_img in enumerate(pages):
        text = pytesseract.image_to_string(page_img, lang="spa")  # Ajusta 'spa' para español, o 'eng' para inglés
        print(f"\n=== Página {i+1} ===")
        print(text)

if __name__ == "__main__":
    pdf_path = "data/pdfs/20CV-152107 - INFORME TÉCNICO CREAS - GREENS SPA.pdf"  # Ajusta si tu PDF se llama distinto
    extract_text_via_ocr(pdf_path)
