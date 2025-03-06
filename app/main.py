from app.classifier import process_ingredients
from app.ingredient_processor import fetch_ingredients_data

if __name__ == '__main__':
    fetch_ingredients_data()
    process_ingredients()
from app.classifier import process_ingredients

print("Iniciando procesamiento de ingredientes...")
result = process_ingredients()
print(f"Resultado del procesamiento: {result}")
