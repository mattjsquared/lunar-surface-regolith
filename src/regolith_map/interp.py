import numpy as np, pyinterp
def build_tree(lons, lats, vals):
  spheroid = pyinterp.geodetic.Spheroid(parameters=(1737000, 0))  # Moon
  tree = pyinterp.RTree(system=spheroid)
  coords = np.vstack((np.asarray(lons).ravel(), np.asarray(lats).ravel())).T
  tree.packing(coords, np.asarray(vals).ravel())
  return tree




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
