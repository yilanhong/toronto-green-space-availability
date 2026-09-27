import csv

input_file = "98-401-X2021007_English_CSV_data.csv"
output_file = "toronto_tracts_filtered.csv"

rows_written = 0

with open(input_file, "r", encoding="utf-8", errors="ignore") as infile, \
     open(output_file, "w", newline="", encoding="utf-8") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow(header)

    geo_level_idx = header.index("GEO_LEVEL")
    alt_geo_idx = header.index("ALT_GEO_CODE")

    for row in reader:
        if row[geo_level_idx] == "Census tract" and row[alt_geo_idx].startswith("535"):
            writer.writerow(row)
            rows_written += 1

print(f"Done. Wrote {rows_written} rows to {output_file}")