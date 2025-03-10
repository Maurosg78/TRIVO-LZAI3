#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def parse_creas_text():
    txt_file = "all_creas_text.txt"  # Ajustado
    output_file = "creas_tables.csv"

    with open(txt_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("linea\n")
        for line in lines:
            if "Tabla" in line:
                safe_line = line.strip().replace(",", ";")
                out.write(f"{safe_line}\n")

    print(f"[DONE] Se ha creado '{output_file}' con líneas que contienen 'Tabla'.")

if __name__ == "__main__":
    parse_creas_text()
