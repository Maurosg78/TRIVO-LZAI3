import pandas as pd

# Función robusta para convertir valores a flotantes
def convert_to_float(value):
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        value = value.strip()
        if value == '' or value == '-':
            return None
        if '<' in value:
            try:
                return float(value.split()[-1])
            except ValueError:
                return None
        try:
            return float(value)
        except ValueError:
            return None
    return None

# Leer el CSV con encabezados y todas las columnas como cadenas
df = pd.read_csv('final_dataset_with_score_NORMALIZED.csv', header=0, quotechar='"', on_bad_lines='skip', encoding='utf-8', dtype=str)

# Lista de columnas numéricas (ajusta según tu archivo)
numeric_cols = [
    'Energy,Regulation EU No 1169/2011 (kJ/100g)', 'energy_kcal', 'Energy,N x Jones\' factor,with fibres (kJ/100g)',
    'Energy,N x Jones\' factor,with fibres (kcal/100g)', 'Water (g/100g)', 'Protein_g_100g', 'Protein,crude,N x 6.25 (g/100g)',
    'Carbs_g_100g', 'Fat_g_100g', 'Sugars (g/100g)', 'fructose (g/100g)', 'galactose (g/100g)', 'glucose (g/100g)',
    'lactose (g/100g)', 'maltose (g/100g)', 'sucrose (g/100g)', 'Starch (g/100g)', 'Fiber_g_100g', 'Polyols (g/100g)',
    'Ash (g/100g)', 'Alcohol (g/100g)', 'Organic acids (g/100g)', 'FA saturated (g/100g)', 'FA mono (g/100g)', 
    'FA poly (g/100g)', 'FA 4:0 (g/100g)', 'FA 6:0 (g/100g)', 'FA 8:0 (g/100g)', 'FA 10:0 (g/100g)', 
    'FA 12:0 (g/100g)', 'FA 14:0 (g/100g)', 'FA 16:0 (g/100g)', 'FA 18:0 (g/100g)', 'FA 18:1 n-9 cis (g/100g)',
    'FA 18:2 9c,12c (n-6) (g/100g)', 'FA 18:3 c9,c12,c15 (n-3) (g/100g)', 'FA 20:4 5c,8c,11c,14c (n-6) (g/100g)',
    'FA 20:5 5c,8c,11c,14c,17c (n-3) EPA (g/100g)', 'FA 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA (g/100g)', 
    'Cholesterol (mg/100g)', 'Salt_g_100g', 'Calcium (mg/100g)', 'Chloride (mg/100g)', 'Copper (mg/100g)', 
    'Iron (mg/100g)', 'Iodine (µg/100g)', 'Magnesium (mg/100g)', 'Manganese (mg/100g)', 'Phosphorus (mg/100g)',
    'Potassium (mg/100g)', 'Selenium (µg/100g)', 'Sodium_mg_100g', 'Zinc (mg/100g)', 'Retinol (µg/100g)',
    'Beta-carotene (µg/100g)', 'Vitamin D (µg/100g)', 'Vitamin E (mg/100g)', 'Vitamin K1 (µg/100g)', 
    'Vitamin K2 (µg/100g)', 'Vitamin C (mg/100g)', 'Vitamin B1 or Thiamin (mg/100g)', 'Vitamin B2 or Riboflavin (mg/100g)',
    'Vitamin B3 or Niacin (mg/100g)', 'Vitamin B5 or Pantothenic acid (mg/100g)', 'Vitamin B6 (mg/100g)',
    'Vitamin B9 or Folate (µg/100g)', 'Vitamin B12 (µg/100g)', 'CARBOHYDRATE,TOTAL (BY DIFFERENCE)', 
    'ENERGY (KILOCALORIES)', 'FAT (TOTAL LIPIDS)', 'FIBRE,TOTAL DIETARY', 'PROTEIN', 'SODIUM', 'score_aceptacion'
]

# Convertir columnas numéricas
for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].apply(convert_to_float)
    else:
        print(f"Advertencia: La columna '{col}' no se encontró en el DataFrame.")

# Manejar valores faltantes (reemplazar None con 0)
df = df.fillna(0)

# Guardar el dataset limpio
df.to_csv('final_dataset_with_score_CLEANED.csv', index=False)
print("Dataset limpio guardado en 'final_dataset_with_score_CLEANED.csv'")