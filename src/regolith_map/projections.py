import cartopy.crs as ccrs
GLOBE = ccrs.Globe(ellipse=None, semimajor_axis=1737000, semiminor_axis=1737000)
PLATE_CARREE = ccrs.PlateCarree(globe=GLOBE)
nearside_laea = ccrs.LambertAzimuthalEqualArea(globe=GLOBE)
farside_laea = ccrs.LambertAzimuthalEqualArea(central_longitude=180, globe=GLOBE)
