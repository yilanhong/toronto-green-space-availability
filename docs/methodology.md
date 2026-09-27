# Methodology

This document describes the full workflow, the reasoning behind key decisions, and the validation steps used throughout the project. All spatial work was completed in ArcGIS Pro using the NAD 1983 CSRS MTM Zone 10 projection.

---

## 1. Green Space Classification

### Source data
The City of Toronto's Green Spaces dataset contains 3,379 polygons covering parks, natural areas, and a wide range of other land types, including cemeteries, golf courses, traffic islands, and building grounds. Not all of these represent publicly accessible green space.

### Definition of green space
For this project, green space had to be publicly accessible, free to enter, and provide meaningful open space and greenery. Features were classified into three mutually exclusive tiers plus an excluded category:

| Category | Description | Examples | Count |
|---|---|---|---|
| **Tier 1** | Formal and manicured parks where recreation or maintained public use is the primary function | Parks, parkettes, playgrounds, sports fields, civic squares | 1,929 |
| **Tier 2** | Natural heritage, natural, and trail spaces valued for their natural character or trail experience | Ravines, creeks, woodlots, wetlands, valleys, trails, beaches | 233 |
| **Tier 3** | Legitimate public green or open space that does not fit Tier 1 or 2, or where green space is a secondary use | Linear parks, hydro corridors, community gardens, community centre grounds | 258 |
| **Excluded** | Features that do not represent meaningful public green space | Cemeteries, golf courses, roads and medians, schools, paid-entry sites, private or restricted land | 959 |

The tiered structure allows the analysis to distinguish *what kind* of green space an area has, not only how much, since a formal park, a ravine, and a hydro corridor offer very different experiences.

### Classification method
Features were classified using SQL attribute queries on the dataset's category (`AREA_CL6`) and name (`AREA_NA9`) fields. Because many names match more than one category (for example, "Taylor Creek Park" contains both "PARK" and "CREEK"), a priority order was applied:

1. **Hard exclusions** (cemeteries, golf courses, roads, schools, paid-entry sites, etc.) always take precedence
2. **Tier 1**
3. **Tier 2**
4. **Tier 3**
5. **Excluded catch-all**: any record matching none of the above

Each category's query includes `AND NOT` clauses for every higher-priority category, so each query can be run independently against the unmodified source layer. The full queries are in [`../queries/tier_classification.sql`](../queries/tier_classification.sql).

An earlier workflow that deleted records from the base layer after each export proved unreliable, producing empty or inconsistent outputs. Replacing it with independent, priority-based queries made the classification fully reproducible and removed any dependence on the order of operations.

### Outlier review
After an initial run, each tier was manually reviewed for keyword false positives. Examples that were corrected:
- `%WOOD%` matched building names such as Harwood Hall, Crestwood College, and Yorkwoods Library (moved to Excluded) and Northwood Community Centre (moved to Tier 3)
- `%VILLAGE%` matched place names such as Victoria Village; the keyword was removed from Tier 1
- Pioneer Village, a paid-entry heritage site, was explicitly excluded

### Validation
- The four category counts sum to exactly 3,379, matching the source total, confirming no records were lost or duplicated
- Keyword spot checks confirmed no remaining cross-category matches (for example, no "Park" names in Tier 2)
- Results were confirmed to persist after closing and reopening the project

The three included tiers were merged into a single layer of 2,420 polygons, each tagged with a `GreenSpace_Type` field. Six invalid geometries (self-intersections and one ring-ordering error) were fixed with **Repair Geometry**.

---

## 2. Census Data Processing

### Variables
Fifteen variables were selected to cover distinct demographic dimensions without overloading the analysis:

| Dimension | Variables |
|---|---|
| Population | Total population, population density, total private dwellings |
| Age | Median age, % aged 0–14, % aged 65+ |
| Income | Median household income (2020), low income prevalence (LIM-AT) |
| Housing | % owner households, % renter households, % apartments in buildings of 5+ storeys |
| Diversity and immigration | % visible minority, % immigrants, % recent immigrants (2016–2021) |
| Employment | Unemployment rate |

### Processing
The Statistics Canada Census Profile file for census tracts (catalogue 98-401-X2021007) is a 2.6 GB CSV in long format, with one row per geography per characteristic. It was processed in Python in two stages:

1. **Filtering** (`scripts/filter_toronto.py`): streamed the file line by line to keep only census tracts in the Toronto CMA (geography codes beginning with `535`), reducing it to about 438 MB
2. **Selection and reshaping** (`scripts/build_final_table_v2.py`): selected the 15 variables and pivoted the table to one row per tract, with count and rate columns for each variable

Several characteristic names appear more than once in the Census Profile because they are reused across tables (for example, "65 years and over" appears in six different tables). These were resolved by inspecting the surrounding characteristics and selecting by unique `CHARACTERISTIC_ID` instead of by name:

| Variable | Characteristic ID | Source table |
|---|---|---|
| 0 to 14 years | 9 | Population by age group |
| 65 years and over | 24 | Population by age group |
| Recent immigrants (2016–2021) | 1536 | Immigrant status and period of immigration |

The output table contains 1,227 Toronto CMA census tracts.

---

## 3. Study Area Definition

1. The census table was joined to the Statistics Canada 2021 census tract boundary file using the `DGUID` field. All 1,227 tracts matched with no null values.
2. A City of Toronto boundary was created by dissolving the City's 174 neighbourhood polygons into a single outline.
3. Tracts were selected if their **centroid** falls within the city boundary, resulting in **577 tracts**.

**Why centroid selection instead of clipping:** census values describe entire tracts. Clipping border tracts to the city boundary would pair a reduced area with a full-tract population, distorting per-resident and coverage measures. Centroid selection keeps every tract whole, so its census data remains valid, while including only tracts that are mostly within the city.

The tract layer was then reprojected from Statistics Canada Lambert to NAD 1983 CSRS MTM Zone 10 to match the green space data.

---

## 4. Spatial Overlay and Aggregation

1. **Intersect** split the green space polygons along census tract boundaries, so each piece carries both its tier and its tract ID
2. **Calculate Geometry** computed the area of each piece in square metres
3. **Summary Statistics** summed green space area by tract and tier, and by tract overall
4. **Pivot Table** reshaped the tier totals to one row per tract
5. The results were joined to the tract layer and exported as a single master table

Tracts with no green space had no intersect output and were set to 0 m². The three tier areas sum to the total green space area in every tract, which served as a consistency check.

---

## 5. Availability Measures

| Measure | Formula | Purpose |
|---|---|---|
| Green space coverage (%) | Green space area ÷ tract land area × 100 | How green the area is overall |
| Tier coverage (%) | Tier area ÷ tract land area × 100 | How much of the tract each tier covers |
| Green space per resident (m²) | Green space area ÷ population | How much green space each resident has |
| Tier share of green space (%) | Tier area ÷ total green space area × 100 | The mix of green space types in a tract |
| Dominant tier | Tier with the largest area in the tract | The main type of green space present |

Tract land area comes from the Statistics Canada `LANDAREA` field (km²) and was converted to m² for these calculations. Tier share is left as null for the 36 tracts with no green space, since the composition of zero green space is undefined; all other measures are 0 for these tracts.

**Summary statistics (577 tracts):**
- Coverage: mean 11.1%, minimum 0%, maximum 83.9%
- Per resident: 25th percentile 3.3 m², median 10.9 m², 75th percentile 33.4 m², maximum 4,714.6 m²

Three tracts exceed 1,000 m² per resident (the Toronto Islands, the Rouge Park and Toronto Zoo area, and one tract west of downtown). These are legitimate values reflecting large parks with small residential populations, so they were retained rather than removed.

---

## 6. Availability Groups

Green space per resident was chosen as the primary measure because the research question concerns availability to residents. Tracts were grouped by quartile:

| Group | Definition | Tracts |
|---|---|---|
| Underserved | Bottom 25% (≤ 3.26 m² per resident) | 144 |
| Moderate | Middle 50% | 288 |
| Well-served | Top 25% (> 33.35 m² per resident) | 145 |

A **severe** flag was added for underserved tracts that are also in the bottom 25% for coverage (≤ 2.66%). This identifies tracts that lack green space outright, rather than only relative to a large population. 122 of the 144 underserved tracts meet this threshold.

Quartiles were chosen because they are simple to explain, data-driven, and produce groups large enough for meaningful comparison.

---

## 7. Demographic Comparison

Demographic variables were summarized for each availability group, for severe versus non-severe tracts, and citywide. Values are **unweighted averages across tracts** (the "average tract" in each group), which is appropriate for comparing groups but differs from true population-wide figures. For example, the mean of tract median incomes is not the city's actual median income.

Results are in `data/summary_tables/Results_Demographic_Comparison.csv`.

---

## 8. Case Studies

Three neighbourhoods were selected to represent low, middle, and high green space availability: **Downtown Yonge East**, **Rustic**, and **Black Creek**. Census tracts were assigned to each neighbourhood by centroid (3, 2, and 5 tracts respectively).

Neighbourhood values were calculated by summing tract counts (green space area, land area, population, households, and population subgroups) and recalculating percentages, which is more accurate than averaging tract percentages. Low income and unemployment use population-weighted averages of tract rates. Because medians cannot be combined exactly, household income is reported as the range across tracts and a population-weighted average.

Results are in `data/summary_tables/Results_CaseStudy_Comparison.csv`.

---

## 9. Visualization

- **Manual class breaks** were used for the coverage and per-resident maps. Automatic methods such as Natural Breaks compressed most tracts into one or two classes because of extreme outliers. Manual breaks give meaningful detail across typical tracts, with a clearly labelled top class for exceptional values.
- **A separate class for zero** highlights tracts with no green space.
- **The composition map** layers bold tier-coloured green space polygons over a pale dominant-tier choropleth, showing both the actual green spaces and the overall character of each tract.
- Charts were produced in Python with matplotlib, with all axes starting at zero to avoid exaggerating differences.

---

## Validation Summary

| Check | Result |
|---|---|
| Classification counts reconcile to source total | 3,379 = 1,929 + 233 + 258 + 959 |
| Merged green space count | 2,420 |
| Census-to-boundary join | 1,227 of 1,227 matched, 0 nulls |
| Study area tracts | 577 |
| Tier areas sum to total area per tract | Confirmed |
| Dominant tier counts reconcile | 495 + 5 + 41 + 36 = 577 |
| Availability groups reconcile | 144 + 288 + 145 = 577 |
| Zero-green-space tracts consistent across fields | 36 |
