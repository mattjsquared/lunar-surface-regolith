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
import pyinterp


def build_tree(lons, lats, vals):
  spheroid = pyinterp.geodetic.Spheroid(parameters=(1737000, 0))  # Moon
  tree = pyinterp.RTree(system=spheroid)
  coords = np.vstack((np.asarray(lons).ravel(), np.asarray(lats).ravel())).T
  tree.packing(coords, np.asarray(vals).ravel())
  return tree




