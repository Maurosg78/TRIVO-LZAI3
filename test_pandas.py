import pandas as pd

# Leer el archivo limpio
df = pd.read_csv('final_dataset_with_score_CLEANED.csv', low_memory=False)

# Mostrar las primeras filas
print(df.head())