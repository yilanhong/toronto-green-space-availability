# Limitations

These limitations should be considered when interpreting the results. Several also point to directions for future work.

## Availability, not accessibility
The analysis measures how much green space exists **within** each census tract. It does not measure how easily residents can reach green space. In practice, people regularly use parks in neighbouring tracts, and a tract with little green space may sit next to a large park. Accessibility would require proximity or network analysis, such as walking distance to the nearest park entrance, which was outside the scope of this project.

## Green space quality is not measured
All green space area is treated equally within each tier. A maintained park with facilities, a steep ravine, and a hydro corridor may contribute similar area but offer very different usability, safety, and amenities. This matters for interpretation: some areas with high availability, such as Black Creek, owe part of their total to utility corridors and valley lands.

## Name-based classification
Tiers were assigned using keywords in feature names and categories. Although results were reviewed and outliers corrected, keyword matching can still misclassify individual features. The priority order also means that **ravine and valley lands officially named as parks are classified as Tier 1**, so natural spaces are likely underrepresented as a dominant tier (only 5 tracts are Tier 2 dominant).

## Per-resident measures are sensitive to density
Dense tracts divide their green space among more people and therefore tend to score lower by definition. The strong association between underserved status and density partly reflects this. The findings are best read as showing that availability is closely shaped by urban form, rather than as evidence that density itself causes lower availability.

## Very small or non-residential populations
Tracts with large parks and small populations produce extreme per-resident values (up to 4,714.6 m² on the Toronto Islands). These values are accurate but can dominate averages, which is why medians and quartiles were used where possible.

## Tract-level averages
Group comparisons use unweighted averages across tracts. They describe the "average tract" in each group rather than the average resident, and averages can hide variation within groups. For example, the underserved group may combine dense downtown tracts with suburban pockets that have different profiles.

## Geographic boundaries
- Census tracts were included if their centroid falls within the City of Toronto, so a small amount of area outside the city is included and some area inside it is excluded
- Case study neighbourhoods were approximated by the census tracts whose centroids fall within them
- Results may change at a different geographic scale, such as neighbourhoods instead of tracts (the modifiable areal unit problem)

## Data limitations
- Census data reflects 2021, while the green space dataset reflects the City's most recent release, so the two do not describe exactly the same point in time
- Statistics Canada suppresses some values for tracts with very small populations, so a small number of tracts may be missing certain variables
- The 2021 Census was collected during the COVID-19 pandemic, which may affect variables such as unemployment and income
- Only City of Toronto green space data was used; privately owned publicly accessible spaces and some other land may not be included

## Descriptive, not causal
The demographic comparisons show patterns and associations. They do not establish that any demographic characteristic causes differences in green space availability, and no statistical significance testing was performed.

## Future work
- Proximity or network analysis (for example, walking distance to the nearest park) to measure accessibility directly
- Incorporating green space quality, such as amenities, tree canopy, or facilities
- Refining the tier classification to separate ravine parks from formal parks
- Statistical testing, such as correlation or regression, of the relationships identified here
