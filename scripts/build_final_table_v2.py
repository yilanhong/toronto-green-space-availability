import pandas as pd

input_file = "toronto_tracts_filtered.csv"

df = pd.read_csv(input_file, dtype=str, low_memory=False)
df["CHARACTERISTIC_ID"] = pd.to_numeric(df["CHARACTERISTIC_ID"], errors="coerce")
df["CHAR_STRIPPED"] = df["CHARACTERISTIC_NAME"].str.strip()

# Characteristics that were uniquely named (safe to match by stripped text)
unique_names = [
    "Population, 2021",
    "Population density per square kilometre",
    "Total private dwellings",
    "Median age of the population",
    "Median total income of household in 2020 ($)",
    "Prevalence of low income based on the Low-income measure, after tax (LIM-AT) (%)",
    "Owner",
    "Renter",
    "Apartment in a building that has five or more storeys",
    "Total visible minority population",
    "Immigrants",
    "Unemployment rate",
]

# Characteristics that were ambiguous - matched by CHARACTERISTIC_ID instead
ambiguous_ids = {
    9: "0 to 14 years",
    24: "65 years and over",
    1536: "Recent immigrants (2016 to 2021)",
}

id_cols = ["DGUID", "ALT_GEO_CODE", "GEO_NAME"]

part1 = df[df["CHAR_STRIPPED"].isin(unique_names)].copy()
part1["LABEL"] = part1["CHAR_STRIPPED"]

part2 = df[df["CHARACTERISTIC_ID"].isin(ambiguous_ids.keys())].copy()
part2["LABEL"] = part2["CHARACTERISTIC_ID"].map(ambiguous_ids)

combined = pd.concat([part1, part2], ignore_index=True)

combined["C1_COUNT_TOTAL"] = pd.to_numeric(combined["C1_COUNT_TOTAL"], errors="coerce")
combined["C10_RATE_TOTAL"] = pd.to_numeric(combined["C10_RATE_TOTAL"], errors="coerce")

pivot_count = combined.pivot_table(index=id_cols, columns="LABEL", values="C1_COUNT_TOTAL", aggfunc="first")
pivot_count.columns = [f"{c}_count" for c in pivot_count.columns]

pivot_rate = combined.pivot_table(index=id_cols, columns="LABEL", values="C10_RATE_TOTAL", aggfunc="first")
pivot_rate.columns = [f"{c}_rate" for c in pivot_rate.columns]

final = pivot_count.join(pivot_rate).reset_index()

final.to_csv("toronto_census_final.csv", index=False)

print(f"Done. {len(final)} census tracts written to toronto_census_final.csv")
print(f"Total columns: {len(final.columns)}")
print(f"Columns: {list(final.columns)}")