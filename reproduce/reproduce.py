#!/usr/bin/env python
import argparse, numpy as np
import pandas as pd, geopandas as gpd
from shapely.geometry import Polygon
from regolith_map.projections import GLOBE, PLATE_CARREE, nearside_laea, farside_laea
from regolith_map.grids import generate_limb_circle, generate_gridpoints
from regolith_map.interp import build_tree
from regolith_map.plotting import generate_projected_axes, apply_rcparams
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe

def main(args):
  apply_rcparams()
  mare = gpd.read_pickle(args.mare)  # your USGSmare.pkl
  mask_ns = gpd.GeoDataFrame(
    geometry=[Polygon(generate_limb_circle().vertices)],
    crs=PLATE_CARREE
  ).to_crs(mare.crs)

  mare_ns = mare.overlay(mask_ns, how='intersection').to_crs(nearside_laea)
  mare_fs = mare.overlay(mask_ns, how='difference').to_crs(farside_laea)

  points = pd.read_excel(args.points)
  # append your “new_points” rows here if needed

  # parse thickness and lat/lon
  thick = points["THICKNESS"].astype(str).str.replace(" m","",regex=False)
  thick = thick.str.split("±|-", expand=True)[0].astype(float).to_numpy()
  lonlat = points["lat, long"].str.split(",", expand=True).astype(float)
  lons = lonlat[0].to_numpy(); lats = lonlat[1].to_numpy()
  lons[lons > 180] -= 360

  # grid + tree
  pts = generate_gridpoints(nlat=args.nlat)
  ctr_lon, ctr_lat = pts["ctr"]["lon"], pts["ctr"]["lat"]
  tree = build_tree(lons, lats, thick)
  idw_vals, _ = tree.inverse_distance_weighting(
    coordinates = np.vstack((ctr_lon.ravel(), ctr_lat.ravel())).T,
    k=9, p=2, within=False
  )
  idw_vals = idw_vals.reshape(ctr_lon.shape)

  # figure
  fig, axs, cax = generate_projected_axes(
    [nearside_laea, farside_laea],
    nrow=1, ncol=2,
    boundaries=generate_limb_circle(),
    map_height=3, ax_titles=['Nearside','Farside'],
    with_cax=True, cax_orientation='horizontal'
  )
  kw_mesh = dict(vmin=2, vmax=10, shading='flat', transform=PLATE_CARREE, zorder=0)
  kw_scatter = dict(s=5, c=thick, vmin=2, vmax=10, linewidths=.5,
                    edgecolors=[1,1,1,1], transform=PLATE_CARREE, zorder=100,
                    path_effects=[pe.SimpleLineShadow(offset=(.4,-.4), alpha=.5), pe.Normal()])

  for a in axs:
    h = a.pcolormesh(pts["edge"]["lon"], pts["edge"]["lat"], idw_vals, **kw_mesh)
    a.scatter(lons, lats, **kw_scatter)
    a.spines['geo'].set_zorder(1000)

  plt.colorbar(h, cax=cax, orientation='horizontal', label='Regolith thickness (m)')
  cax.minorticks_on()
  if args.out:
    plt.savefig(args.out, bbox_inches='tight', dpi=600)
  plt.show()

if __name__ == "__main__":
  p = argparse.ArgumentParser()
  p.add_argument("--mare",   default="data/USGSmare.pkl")
  p.add_argument("--points", default="data/for_matt.xlsx")
  p.add_argument("--nlat", type=int, default=20)
  p.add_argument("--out",  default=None)
  main(p.parse_args())
