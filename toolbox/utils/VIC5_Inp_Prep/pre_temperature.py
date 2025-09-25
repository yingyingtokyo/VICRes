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
input_dir = os.path.join(main_dir, "download", "temperature")
output_file = os.path.join(main_dir, "preprocess", "era5_t2m_2005-2020.nc")

# Open input files
dt1 = xr.open_dataset(os.path.join(input_dir, "era5_t2m_2004-2012.nc"))
dt2 = xr.open_dataset(os.path.join(input_dir, "era5_t2m_2013-2020.nc"))
dt = xr.concat([dt1, dt2], dim = "valid_time")
dt = dt.sortby('latitude') 

# Change time zone by +7 hours for the Mekong
dt = dt.assign_coords(valid_time = dt.valid_time + pd.Timedelta(hours = 7))
# Slice by time
dt = dt.sel(valid_time=slice(sta_date, end_date))

# Access varibale (temperature K)
t2m_k = dt["t2m"] 

# Convert temperature from K to °C
t2m_c = t2m_k - 273.15

# Regrid using neareast method
new_lat = np.arange(min_lat, max_lat + reso, reso)
new_lon = np.arange(min_lon, max_lon + reso, reso)
op = t2m_c.interp(latitude = new_lat, longitude = new_lon, method="nearest")

# Export output file
op.to_netcdf(output_file, encoding = {"t2m": {"zlib": True, "complevel": 4}})