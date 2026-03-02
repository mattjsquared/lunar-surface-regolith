# Copyright (C) 2026 Matthew Jones and Andrea Rajšić
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
import pandas as pd
import pyinterp


def build_tree(lons, lats, vals):
  spheroid = pyinterp.geodetic.Spheroid(parameters=(1737000, 0))  # Moon
  tree = pyinterp.RTree(system=spheroid)
  coords = np.vstack((np.asarray(lons).ravel(), np.asarray(lats).ravel())).T
  tree.packing(coords, np.asarray(vals).ravel())
  return tree


def interpolate_at_points(data_vals, data_lats, data_lons, interp_lats, interp_lons, method='rbf', body='moon', return_tree=False, **kwargs):
  '''
  
  '''
  # Define initial data shapes
  data_shape = np.shape(data_vals)
  interp_shape = np.shape(interp_lats)
  # Enforce shape consistency
  if not all([np.shape(x) == data_shape for x in [data_lats, data_lons]]):
    raise ValueError(f"Shapes of `data_lats` ({np.shape(data_lats)}) and `data_lons` ({np.shape(data_lons)}) must match shape of `data_vals` ({data_shape}).")
  if np.shape(interp_lons) != interp_shape:
    raise ValueError(f"Shapes of `interp_lats` ({interp_shape}) and `interp_lons` ({np.shape(interp_lons)}) must match.")
  # Force data into flattened ndarrays
  data_vals = np.asarray(data_vals).ravel()
  data_lats = np.asarray(data_lats).ravel()
  data_lons = np.asarray(data_lons).ravel()
  interp_lats = np.asarray(interp_lats).ravel()
  interp_lons = np.asarray(interp_lons).ravel()
  # Initialize pyinterp
  if body.lower() == 'moon':
    spheroid = pyinterp.geodetic.Spheroid(parameters=(1737000, 0))
  else:
    raise NotImplementedError("The Moon is currently the only supported `body`.")
  coords = np.vstack((data_lons, data_lats)).T
  queries = np.vstack((interp_lons, interp_lats)).T
  tree = pyinterp.RTree(system=spheroid)
  tree.packing(coords, data_vals)
  
  # Select method and compute interpolated values
  method = method.replace('_', ' ')
  if method in ['nn', 'nearest', 'nearest neighbor', 'value']:
    _, interp_vals = tree.value(queries, **kwargs)
  else:
    if method in ['idw', 'inverse distance', 'inverse distance weighting']:
      interp_func = tree.inverse_distance_weighting
    elif method in ['rbf', 'radial basis', 'radial basis function']:
      interp_func = tree.radial_basis_function
    elif method in ['krig', 'kriging', 'universal kriging']:
      interp_func = tree.universal_kriging
    interp_vals, _ = interp_func(queries, **kwargs)
  # Put the results into the shape of the input coordinates and return
  interp_vals = np.reshape(interp_vals, interp_shape)
  if return_tree:
    return interp_vals, tree
  else:
    return interp_vals


def spherical_centroid(lat_deg, lon_deg):
  lat = np.radians(lat_deg)
  lon = np.radians(lon_deg)

  x = np.cos(lat) * np.cos(lon)
  y = np.cos(lat) * np.sin(lon)
  z = np.sin(lat)

  x_m, y_m, z_m = x.mean(), y.mean(), z.mean()

  lon_c = np.arctan2(y_m, x_m)
  hyp = np.sqrt(x_m**2 + y_m**2)
  lat_c = np.arctan2(z_m, hyp)

  return np.degrees(lat_c), np.degrees(lon_c)

