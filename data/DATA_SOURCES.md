# Data Sources

| Dataset | Publisher | Use in this project | Link |
|---|---|---|---|
| Green Spaces | City of Toronto Open Data | Green space polygons, classified into tiers | https://open.toronto.ca/dataset/green-spaces/ |
| Neighbourhoods (current 174-neighbourhood boundaries) | City of Toronto Open Data | City boundary (dissolved) and case study areas | https://open.toronto.ca/dataset/neighbourhoods/ |
| 2021 Census Tract Boundary File (digital, shapefile) | Statistics Canada | Census tract geometry | https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/index2021-eng.cfm?year=21 |
| Census Profile, 2021 Census of Population: CMAs, tracted CAs and census tracts (98-401-X2021007) | Statistics Canada | Demographic variables | https://www150.statcan.gc.ca/n1/en/catalogue/98-401-X2021007 |

Raw data is not included in this repository because of file size (the Census Profile file alone is 2.6 GB). All datasets can be downloaded from the links above. The `summary_tables/` folder contains the derived results used in the maps and charts.

## Licences and attribution

- Contains information licensed under the Open Government Licence – Toronto.
- Adapted from Statistics Canada, 2021 Census of Population and 2021 Census Tract Boundary File. This does not constitute an endorsement by Statistics Canada of this product. Statistics Canada data is used under the Statistics Canada Open Licence.
- Basemap: Esri Light Gray Canvas (credits shown on each map).

## Projection

All spatial data was processed in NAD 1983 CSRS MTM Zone 10.
