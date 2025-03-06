import pdfplumber
import json
import re

# Ajusta estas listas a los términos que aparezcan en tus informes
KEYWORDS_INGREDIENT = ["ingrediente", "harina", "almidon", "aceite", "garbanzo"]
KEYWORDS_COST = ["costo", "coste"]
KEYWORDS_NUTRIENTS = ["proteina", "fiber", "fibra", "sodio"]

FORM_DATA = {
    "project_info": {
        "project_name": "",
        "date_of_report": "",
        "client": "",
        "location": ""
    },
    "ingredients": [],
    "process_parameters": {}
}

def extract_data_from_pdf(pdf_path):
    data_extracted = {
        "ingredients": [],
        "notes": []  # Guardar texto relevante que no se haya parseado directamente
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            lines = text.split('
') if text else []

            for line in lines:
                # Busca patrones de ingredientes
                if any(kw.lower() in line.lower() for kw in KEYWORDS_INGREDIENT):
                    data_extracted["ingredients"].append({
                        "line": line,
                        "page": page_number
                    })
                # Otras búsquedas...
                elif any(kw.lower() in line.lower() for kw in KEYWORDS_COST):
                    data_extracted["notes"].append({
                        "line": line,
                        "page": page_number,
                        "type": "cost"
                    })
                elif any(kw.lower() in line.lower() for kw in KEYWORDS_NUTRIENTS):
                    data_extracted["notes"].append({
                        "line": line,
                        "page": page_number,
                        "type": "nutrients"
                    })

    return data_extracted


def main():
    pdf_path = "PATH/TO/YOUR/CREAS_REPORT.pdf"  # Ajusta a la ruta real
    results = extract_data_from_pdf(pdf_path)

    # Aquí ya tienes "results" con líneas que contienen las palabras clave.
    # Deberás parsear esas líneas para extraer la info (por ejemplo, regex o splits)

    with open("creas_extracted.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Datos extraídos y guardados en creas_extracted.json")

if __name__ == "__main__":
    main()

