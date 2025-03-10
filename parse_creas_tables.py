#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def parse_creas_tables():
    txt_file = "data/pdfs/all_creas_text.txt"
    output_file = "creas_tables_details.csv"

    with open(txt_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    out = open(output_file, "w", encoding="utf-8")
    out.write("tabla_id,contenido\n")

    capture_mode = False
    table_id = ""
    lines_captured = []

    for line in lines:
        # Detectamos la línea con "Tabla X.Y"
        if "Tabla " in line:
            # Si ya estábamos capturando otra tabla, la cerramos
            if capture_mode and lines_captured:
                for lc in lines_captured:
                    safe_lc = lc.strip().replace(",", ";")
                    out.write(f"{table_id},{safe_lc}\\n")
                # Limpiamos
                lines_captured = []

            # Iniciar captura para la nueva tabla
            table_id = line.strip().replace(",", ";")  # p.ej. "Tabla 3.1..."
            capture_mode = True
            continue

        if capture_mode:
            # Condición de salida: línea en blanco o "===" indica fin de tabla
            if line.strip() == "" or "===" in line:
                # Guardar lo capturado
                for lc in lines_captured:
                    safe_lc = lc.strip().replace(",", ";")
                    out.write(f"{table_id},{safe_lc}\\n")
                capture_mode = False
                lines_captured = []
                table_id = ""
            else:
                # Vamos capturando líneas de la tabla
                lines_captured.append(line)

    # Si el archivo terminó mientras capturábamos tabla
    if capture_mode and lines_captured:
        for lc in lines_captured:
            safe_lc = lc.strip().replace(",", ";")
            out.write(f"{table_id},{safe_lc}\\n")

    out.close()
    print(f"[DONE] Se ha creado '{output_file}' con el contenido de las tablas.")

if __name__ == "__main__":
    parse_creas_tables()
