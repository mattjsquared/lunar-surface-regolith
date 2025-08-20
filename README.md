# Lunar Surface Regolith Thickness Mapping

[![DOI](https://zenodo.org/badge/1036316580.svg)](https://doi.org/10.5281/zenodo.16912357)

**Version:** 1.0.1

This package provides tools for estimating and mapping global lunar surface regolith thickness as in [Rajšić et al. (2025)](), using spatial interpolation from scattered measurements.

## Features

- Loads and parses regolith thickness measurements from CSV/Excel files.
- Interpolates thickness values across the lunar surface using inverse distance weighting (IDW) with a spherical R-tree.
- Visualizes global and hemispheric maps with customizable projections.
- Overlays mare regions using USGS lunar maria shapefiles.
- Generates publication-quality figures with matplotlib and cartopy.

## Citation

If you use this package, please cite:

Matt J. Jones & Andrea Rajšić (2025). Lunar Surface Regolith Thickness Mapping (Version 1.0.1) [Software]. https://github.com/mattjsquared/lunar-surface-regolith  
DOI: [10.5281/zenodo.16912534](https://doi.org/10.5281/zenodo.16912534)

BibTeX:
@misc{jones2025regolith,
  author = {Jones, Matt J. and Rajšić, Andrea},
  title = {Lunar Surface Regolith Thickness Mapping},
  year = {2025},
  version = {1.0.1},
  doi = {10.5281/zenodo.16912358},
  url = {https://doi.org/10.5281/zenodo.16912534}
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
conda activate grl-regolith
```

## Usage

To reproduce the main figures, from the `lunar-surface-regolith/` directory, run:

```bash
python reproduce/reproduce.py
```

Optional command line arguments:

- `--mare`: Path to pickled USGS mare GeoDataFrame (default: `data/USGSmare.pkl`)
- `--data`: Path to regolith measurements file (default: `data/regolith_measurements.xlsx` downloaded from [Rajšić et al. (2025)]())
- `--nlat`: Number of latitude grid divisions (default: 20)
- `--style`: Matplotlib style file (default: `regolith_map.mplstyle`)
- `--out`: Output directory for figures (default: `img/`)

Example:

```bash
python reproduce/reproduce.py --nlat 40 --out results/
```

## Data

- **Regolith measurements**: To reproduce Figure 5 of [Rajšić et al. (2025)](), download Dataset 1 from the Supporting Information and place it in the `reproduce/data/` directory. For custom data, provide a CSV/Excel file (columns: value, longitude, latitude) and specify its path via the `--data` command line argument.
- **USGS mare shapefile**: Provided as a pickled GeoDataFrame, `data/USGSmare.pkl` (pickled using Geopandas v1.1.1). The geometry is the union of all mare units in the vectorized [USGS 1:5,000,000 Geological Map of the Moon](https://astrogeology.usgs.gov/search/map/unified_geologic_map_of_the_moon_1_5m_2020) ([Fortezzo et al., 2020](https://www.hou.usra.edu/meetings/lpsc2020/pdf/2760.pdf)).

## Modules

- `regolith_map.projections`: Lunar map projections for cartopy.
- `regolith_map.helpers`: Utility functions for parsing data and generating masks.
- `regolith_map.interp`: Spherical spatial interpolation using pyinterp.
- `regolith_map.plotting`: Figure and axes generation for lunar maps.

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
