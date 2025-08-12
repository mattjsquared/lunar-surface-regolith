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

#!/usr/bin/env python
import argparse
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

from shapely.geometry import Polygon
from matplotlib import patheffects as pe

import sys, os
SCRIPTDIR = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, os.path.abspath(os.path.join(SCRIPTDIR, '..', 'src')))
from regolith_map.projections import GLOBE, PLATE_CARREE, LAEA_NS, LAEA_FS
from regolith_map.helpers import parse_measurements, generate_limb_circle, generate_gridpoints, generate_nearside_mask
from regolith_map.interp import build_tree
from regolith_map.plotting import generate_projected_axes

def main(args):
  ### Prep the script
  if args.out and not os.path.exists(args.out):
    os.makedirs(args.out)

  ### Prep for plotting mare
  # open the pickled mare GeoDataFrame
  with open(args.mare, 'rb') as f:
    mare = pickle.load(f)
  # generate nearside hemisphere mask
  mask_ns = generate_nearside_mask(mare.crs)
  # clip the mare patches
  mare_ns = mare.overlay(mask_ns, how='intersection').to_crs(LAEA_NS)
  mare_fs = mare.overlay(mask_ns, how='difference').to_crs(LAEA_FS)

  ### Load measurement data
  # read data file
  if args.data.endswith('.csv'):
    data = pd.read_csv(args.data)
  elif args.data.endswith('.xlsx') or args.data.endswith('.xls'):
    data = pd.read_excel(args.data)
  else:
    raise ValueError("Unsupported file input. You may need to manually download Supplemental Dataset 1 into `lunar-surface-regolith/reproduce/data/`.")

  # parse thickness and lat/lon
  data['thickness'] = parse_measurements(data['thickness']).astype(float)
  data['lon'] = data['lon'].astype(float)
  data['lon'][data['lon'] > 180] -= 360
  data['lat'] = data['lat'].astype(float)

  ### IDW estimation
  # prep map grid
  pts = generate_gridpoints(nlat=args.nlat)
  ctr_lon, ctr_lat = pts["ctr"]["lon"], pts["ctr"]["lat"]
  # prep estimation RTree
  tree = build_tree(data.lon, data.lat, data.thickness)
  # do the IDW estimation
  idw_vals, _ = tree.inverse_distance_weighting(
    coordinates = np.vstack((ctr_lon.ravel(), ctr_lat.ravel())).T,
    k=9, p=2, within=False
  )
  idw_vals = idw_vals.reshape(ctr_lon.shape)

  ### Plot maps
  # define format parameters
  plt.style.use(args.style)
  limb_circle = generate_limb_circle()
  kw_ax = dict(
    nrow=1, ncol=2, 
    boundaries=limb_circle, 
    map_height=3, 
    ax_titles=['Nearside','Farside'], 
    with_cax=True, cax_orientation='horizontal'
  )
  kw_map = dict(
    vmin=2, vmax=10,
    shading='flat', 
    transform=PLATE_CARREE, 
    zorder=0
  )
  kw_measurements = dict(
    s=5,
    vmin=kw_map.get('vmin'), vmax=kw_map.get('vmax'), 
    linewidths=.5,
    edgecolors=[1,1,1,1],
    transform=PLATE_CARREE,
    zorder=100,
    path_effects=[pe.SimpleLineShadow(offset=(.4,-.4), alpha=.5), pe.Normal()]
  )
  kw_mare = dict(
    edgecolor=[1, 1, 1, 0],
    facecolor=[.8, .8, .8, .6],
    zorder=1
  )

  # map with mare patch
  fig, axs, cax = generate_projected_axes([LAEA_NS, LAEA_FS], **kw_ax)
  for a in axs:
    h = a.pcolormesh(pts["edge"]["lon"], pts["edge"]["lat"], idw_vals, **kw_map) # plot gridded map
    a.scatter(data.lon, data.lat, c=data.thickness, **kw_measurements) # add measurement points
    a.spines['geo'].set_zorder(1000)
  mare_ns.plot(ax=axs[0], **kw_mare) # display nearside maria
  mare_fs.plot(ax=axs[1], **kw_mare) # display farside maria
  plt.colorbar(h, cax=cax, orientation='horizontal', label='Regolith thickness (m)')
  cax.minorticks_on()
  if args.out:
    plt.savefig(args.out+'lunar_surface_regolith_with_mare.png', bbox_inches='tight')

  # map without mare patch
  fig, axs, cax = generate_projected_axes([LAEA_NS, LAEA_FS], **kw_ax)
  for a in axs:
    h = a.pcolormesh(pts["edge"]["lon"], pts["edge"]["lat"], idw_vals, **kw_map) # plot gridded map
    a.scatter(data.lon, data.lat, **kw_measurements) # add measurement points
    a.spines['geo'].set_zorder(1000)
  plt.colorbar(h, cax=cax, orientation='horizontal', label='Regolith thickness (m)')
  cax.minorticks_on()
  if args.out:
    plt.savefig(args.out+'lunar_surface_regolith.png', bbox_inches='tight')
  plt.show()

if __name__ == "__main__":
  p = argparse.ArgumentParser()
  p.add_argument("--mare",   default=SCRIPTDIR+"data/USGSmare.pkl")
  p.add_argument("--data", default=SCRIPTDIR+"data/regolith_measurements.xlsx")
  p.add_argument("--nlat", type=int, default=20)
  p.add_argument("--style", default=SCRIPTDIR+"regolith_map.mplstyle")
  p.add_argument("--out",  default=SCRIPTDIR+'img/')
  main(p.parse_args())
