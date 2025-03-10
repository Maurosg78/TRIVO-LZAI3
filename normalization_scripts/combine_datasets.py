import pandas as pd

# Definir las rutas de los archivos (ajústalas si es necesario)
MASTER_FILE = '/Users/mauriciosobarzo/Desktop/2025/Greensy/Lanzadera/TRIVO-LZAI3/master_dataset_full.csv'
NORMALIZED_FILE = '/Users/mauriciosobarzo/Desktop/2025/Greensy/Lanzadera/TRIVO-LZAI3/final_dataset_with_score_NORMALIZED.csv'
OUTPUT_FILE = 'master_dataset_updated.csv'

# Paso 1: Cargar ambos datasets
master_df = pd.read_csv(MASTER_FILE, quotechar='"', on_bad_lines='skip', encoding='utf-8')
normalized_df = pd.read_csv(NORMALIZED_FILE, quotechar='"', on_bad_lines='skip', encoding='utf-8', low_memory=False)
# Paso 2: Seleccionar columnas comunes
common_columns = master_df.columns.intersection(normalized_df.columns)
master_df = master_df[common_columns]
normalized_df = normalized_df[common_columns]

# Paso 3: Combinar ambos datasets verticalmente
combined_df = pd.concat([master_df, normalized_df], ignore_index=True)

# Paso 4: Eliminar duplicados basados en 'FoodID' si existe
if 'FoodID' in combined_df.columns:
    combined_df = combined_df.drop_duplicates(subset=['FoodID'])
else:
    combined_df = combined_df.drop_duplicates()

# Paso 5: Guardar el dataset combinado
combined_df.to_csv(OUTPUT_FILE, index=False)
print(f"Dataset combinado guardado en '{OUTPUT_FILE}'")