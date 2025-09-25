# Libraries
import os
import numpy as np
import xarray as xr
import pandas as pd

# Spatial domain
min_lat = 18.9189
max_lat = 33.7939
min_lon = 93.9069
max_lon = 102.0319
reso = 0.0625 # degree

# Temporal domain
sta_date = "2005-01-01"
end_date = "2020-12-31"

# Directories
main_dir = os.getcwd()
input_dir = os.path.join(main_dir, "download", "radiation") 
output_file_sw = os.path.join(main_dir, "preprocess", "era5_sdswrf_2005-2020.nc")
output_file_lw = os.path.join(main_dir, "preprocess", "era5_sdlwrf_2005-2020.nc")

# Open input files
dts1 = xr.open_dataset(os.path.join(input_dir, "era5_sdswrf_2004-2012.nc"))
dts2 = xr.open_dataset(os.path.join(input_dir, "era5_sdswrf_2013-2020.nc"))
dts = xr.concat([dts1, dts2], dim="valid_time")
dts = dts.sortby('latitude') 
dtl1 = xr.open_dataset(os.path.join(input_dir, "era5_sdlwrf_2004-2012.nc"))
dtl2 = xr.open_dataset(os.path.join(input_dir, "era5_sdlwrf_2013-2020.nc"))
dtl = xr.concat([dtl1, dtl2], dim="valid_time")
dtl = dtl.sortby('latitude') 

# Change time zone by +7 hours for the Mekong
dts = dts.assign_coords(valid_time=dts.valid_time + pd.Timedelta(hours=7))
dtl = dtl.assign_coords(valid_time=dtl.valid_time + pd.Timedelta(hours=7))
# Slice by time
dts = dts.sel(valid_time=slice(sta_date, end_date))
dtl = dtl.sel(valid_time=slice(sta_date, end_date))

# Access variable
sw = dts["avg_sdswrf"]  
lw = dtl["avg_sdlwrf"]  

# Regrid using neareast method
new_lat = np.arange(min_lat, max_lat + reso, reso)
new_lon = np.arange(min_lon, max_lon + reso, reso)
ops = sw.interp(latitude = new_lat, longitude = new_lon, method="nearest")
opl = lw.interp(latitude = new_lat, longitude = new_lon, method="nearest")

# Export output files
ops.to_netcdf(output_file_sw, encoding = {"avg_sdswrf": {"zlib": True, "complevel": 4}})
opl.to_netcdf(output_file_lw, encoding = {"avg_sdlwrf": {"zlib": True, "complevel": 4}})