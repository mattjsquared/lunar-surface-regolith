# Lunar Surface Regolith Thickness Mapping

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16912357.svg)](https://doi.org/10.5281/zenodo.16912357)

**Version:** 2.0.0 (2026-03-01)

This package provides tools for estimating and mapping global lunar surface regolith thickness as in [Rajšić et al. (2026)](), using spatial interpolation from scattered measurements.

## Features

- Loads and parses regolith thickness measurements from CSV/Excel files.
- Interpolates thickness values across the lunar surface using inverse distance weighting (IDW) with a spherical R-tree.
- Visualizes global and hemispheric maps with customizable projections.
- Overlays mare regions using USGS lunar maria shapefiles.
- Generates publication-quality figures with matplotlib and cartopy.

## Citation

If you use this package, please cite:

Matt J. Jones & Andrea Rajšić (2026). Lunar Surface Regolith Thickness Mapping (Version 2.0.0) [Software]. https://github.com/mattjsquared/lunar-surface-regolith  
DOI: [10.5281/zenodo.18829373](https://doi.org/10.5281/zenodo.18829373)

BibTeX:
@misc{jones2026regolith,
  author = {Jones, Matt J. and Rajšić, Andrea},
  title = {Lunar Surface Regolith Thickness Mapping},
  year = {2026},
  version = {2.0.0},
  doi = {10.5281/zenodo.18829373},
  url = {https://doi.org/10.5281/zenodo.18829373}
}

## Installation

1. Clone the repository. From the terminal:

```bash
git clone https://github.com/mattjsquared/lunar-surface-regolith.git
cd lunar-surface-regolith
```

2. Create and activate the python environment from the provided `environment.yml` using [conda](https://docs.conda.io/):

```bash
conda env create -f environment.yml
conda activate lunar-surface-regolith
```

## Reproducing [Rajšić et al. (2026)]() geospatial analyses

To reproduce figures from the publication, from the `lunar-surface-regolith/` directory, run:

```bash
jupyter lab
```

Open `reproduce/reproduce.ipynb` and run the cells to generate the maps and statistics. The notebook is structured to allow easy modification of parameters and data paths for custom analyses.

### Data

- **LROC maria shapefile**: Vectorized mare outlines, included as `reproduce/data/LROC_GLOBAL_MARE_180/*`. This data comes from [Speyerer et al. (2011)](http://adsabs.harvard.edu/abs/2011LPI....42.2387S). Used for masking mare regions in the maps.
- **LROC WAC gridded data**: Pickled data for the basemap of the lunar surface, included as `reproduce/data/map_wac.pkl`. Includes variables `wac_lon`, `wac_lat`, and `wac_vals` for longitude, latitude, and data values, respectively.
- **Crater dataset**: Mapped and classified craters from [Rajšić et al. (2026)](). These data are used for estimating regolith thickness based on crater size and REC/nREC classification. The dataset is included in the repository as `reproduce/data/Rajsic-etal2026-PSJ_Table_SM1-SM2.xlsx`.
- **Regolith measurements**: Previously published regolith thickness estimates at points across the lunar surface. Used to generate the IDW-interpolated map of [Rajšić et al. (2026)]() alongside estimates from our crater analysis. Included in the repository as `reproduce/data/RegolithData_Literature.xlsx`.
- **USGS mare shapefile**: Provided as a pickled GeoDataFrame, `reproduce/data/USGSmare.pkl` (pickled indirectly using Geopandas v1.1.1). The geometry is the union of all mare units in the vectorized [USGS 1:5,000,000 Geological Map of the Moon](https://astrogeology.usgs.gov/search/map/unified_geologic_map_of_the_moon_1_5m_2020) ([Fortezzo et al., 2020](https://www.hou.usra.edu/meetings/lpsc2020/pdf/2760.pdf)). Provided as an alternative to the LROC maria shapefile used in [Rajšić et al. (2026)]().

### Cached data

Some of the analyses in `reproduce.ipynb` can take a while to run; `reproduce/cache/` contains pickled `ndarray` caches that are used for plotting some of the figures.

- `bootstraps_highlands_1k.pkl`: 1000 bootstrap resamples of the highlands regolith thickness distribution, used for plotting the bootstrapped confidence intervals.
- `bootstraps_mare_1k.pkl`: 1000 bootstrap resamples of the mare regolith thickness distribution, used for plotting the bootstrapped confidence intervals.
- `permutations_10k.pkl`: 10,000 mare-highlands regolith thickness estimate differences from 10,000 random permutations of the mare/highlands crater labels, used for plotting the permutation test results.
- `rarefaction_highlands_200x1.pkl`: 200 rarefaction resamples (per $k$ for a $k$-interval of 1) of the highlands regolith thickness estimate, used for plotting the rarefaction curves.
- `rarefaction_mare_200x1.pkl`: 200 rarefaction resamples (per $k$ for a $k$-interval of 1) of the mare regolith thickness estimate, used for plotting the rarefaction curves.

## Modules

- `regolith_map.projections`: Lunar map projections for cartopy.
- `regolith_map.helpers`: Utility functions for parsing data and generating masks.
- `regolith_map.interp`: Spherical spatial interpolation using pyinterp.
- `regolith_map.plotting`: Figure and axes generation for lunar maps.
- `regolith_map.estimation`: Functions for estimating regolith thickness and calculating statistics.

## Requirements

See `environment.yml` for all dependencies. Main packages:

- numpy
- matplotlib
- pandas
- geopandas
- cartopy
- shapely
- pyinterp

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE.txt](LICENSE.txt) file for details.

## Contact

For questions or contributions, contact matthew_jones@brown.edu or andrea_rajsic@brown.edu.
