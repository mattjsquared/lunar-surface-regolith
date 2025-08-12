# Copyright (C) 2025 Matthew Jones and Andrea Rajšić
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy as np
import matplotlib as mpl
import geopandas as gpd

from shapely import Polygon
from regolith_map.projections import PLATE_CARREE


def parse_measurements(measurements):
  parsed = []
  for m in measurements:
    parsed.append(float( m.strip(' m').split('-')[0].split('±')[0] ))
  return np.array(parsed)


def generate_limb_circle():
  rect = mpl.path.Path([[-90,-90],[90,-90],[90,90],[-90,90],[-90,-90]]).interpolated(100)
  return rect


def generate_gridpoints(nlat=20):
  nlon = nlat*2
  elon = np.linspace(-180, 180, nlon+1)
  elat = np.linspace(-90,  90, nlat+1)
  edge_lon, edge_lat = np.meshgrid(elon, elat)
  clon = 0.5*(elon[:-1]+elon[1:]); clat = 0.5*(elat[:-1]+elat[1:])
  ctr_lon, ctr_lat = np.meshgrid(clon, clat)
  return {
    "edge": {"lon": edge_lon, "lat": edge_lat,
             "stack": np.vstack((edge_lon.ravel(), edge_lat.ravel())).T},
    "ctr":  {"lon": ctr_lon,  "lat": ctr_lat,
             "stack": np.vstack((ctr_lon.ravel(),  ctr_lat.ravel())).T}
  }


def generate_nearside_mask(crs=PLATE_CARREE):
  mask_ns = gpd.GeoDataFrame(
    geometry=[Polygon(generate_limb_circle().vertices)],
    crs=PLATE_CARREE
  ).to_crs(crs)
  return mask_ns
