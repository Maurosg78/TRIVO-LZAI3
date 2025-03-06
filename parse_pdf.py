import pdfplumber
import json
import os

def parse_pdf(pdf_path):
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                for line in text.split('\n'):
                    lines.append({
                        'page': page_index,
                        'text': line
                    })
    return lines

def main():
    # Ajusta el nombre del PDF que deseas procesar
    pdf_name = '20CV-152107 - INFORME TÉCNICO CREAS - GREENS SPA.pdf'
    pdf_path = f'/Users/mauriciosobarzo/Desktop/2025/Greensy/Lanzadera/TRIVO-LZAI3/data/pdfs/{pdf_name}'

    if not os.path.exists(pdf_path):
        print(f'El archivo PDF no se encuentra en la ruta: {pdf_path}')
        return

    extracted_lines = parse_pdf(pdf_path)

    output_json = 'extracted_data.json'
    with open(output_json, 'w') as f:
        json.dump(extracted_lines, f, indent=4)

    print(f'Proceso completado. Se guardaron {len(extracted_lines)} líneas en {output_json}')

if __name__ == '__main__':
    main()

