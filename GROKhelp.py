import csv

input_file = 'final_dataset_with_score.csv'
output_file = 'final_dataset_with_score_NORMALIZED.csv'

with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)  # Quote all fields
    
    # Escribir la primera fila (encabezados)
    headers = next(reader)
    writer.writerow(headers)
    
    # Escribir el resto de las filas
    for row in reader:
        writer.writerow(row)