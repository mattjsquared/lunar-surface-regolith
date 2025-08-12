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
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs

from regolith_map.projections import GLOBE


def generate_projected_axes(projections, nrow=1, ncol=1, boundaries=None,
                            map_height=3, ax_titles=None, with_cax=True,
                            cax_ratio=0.08, cax_orientation='horizontal',
                            kw_fig={}, kw_gspec={}, kw_ax={}):
  nax = nrow*ncol
  if isinstance(projections, ccrs.Projection): projections=[projections]*nax
  projections = np.reshape(projections,(nrow,ncol)).astype(ccrs.Projection)

  kw_fig.setdefault('facecolor',[1,1,1,0])
  kw_gspec.setdefault('hspace',0.05); kw_gspec.setdefault('wspace',0.05)
  kw_ax.setdefault('facecolor',[1,1,1,0])

  fig_h, fig_w = map_height*nrow, map_height*ncol
  nrow_gspec, ncol_gspec = nrow, ncol
  hratios, wratios = [1]*nrow, [1]*ncol
  if with_cax:
    adj = cax_ratio*map_height
    if cax_orientation=='horizontal':
      fig_h += adj; nrow_gspec += 1; hratios.append(cax_ratio)
    else:
      fig_w += adj; ncol_gspec += 1; wratios.append(cax_ratio)

  fig = plt.figure(figsize=(fig_w,fig_h), **kw_fig)
  gs = fig.add_gridspec(nrow_gspec, ncol_gspec, height_ratios=hratios, width_ratios=wratios, **kw_gspec)

  ax = np.empty((nrow,ncol)).astype(plt.Axes)
  for i in range(nrow):
    for j in range(ncol):
      a = fig.add_subplot(gs[i,j], projection=projections[i,j], **kw_ax)
      if boundaries is not None:
        clon = a.projection.proj4_params.get('lon_0')
        tf = ccrs.PlateCarree(central_longitude=clon, globe=GLOBE)
        a.set_boundary(boundaries, transform=tf)
        v = boundaries.vertices
        a.set_extent([v[:,0].min(), v[:,0].max(), v[:,1].min(), v[:,1].max()], crs=tf)
      if ax_titles is not None: a.set_title(ax_titles[i*ncol+j])
      ax[i,j]=a

  cax = None
  if with_cax:
    cax = fig.add_subplot(gs[-1,:] if cax_orientation=='horizontal' else gs[:, -1])
  return fig, ax.ravel(), cax
