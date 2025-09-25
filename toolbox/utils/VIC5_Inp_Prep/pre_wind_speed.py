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
input_dir = os.path.join(main_dir, "download", "wind_speed") 
output_file = os.path.join(main_dir, "preprocess", "era5_w10_2005-2020.nc")

# Open NetCDF files
dtu1 = xr.open_dataset(os.path.join(input_dir, "era5_u10_2004-2012.nc"))
dtu2 = xr.open_dataset(os.path.join(input_dir, "era5_u10_2013-2020.nc"))
dtu = xr.concat([dtu1, dtu2], dim="valid_time")
dtu = dtu.sortby('latitude') 
dtv1 = xr.open_dataset(os.path.join(input_dir, "era5_v10_2004-2012.nc"))
dtv2 = xr.open_dataset(os.path.join(input_dir, "era5_v10_2013-2020.nc"))
dtv = xr.concat([dtv1, dtv2], dim="valid_time")
dtv = dtv.sortby('latitude') 

# Change time zone by +7 hours for the Mekong
dtu = dtu.assign_coords(valid_time=dtu.valid_time + pd.Timedelta(hours=7))
dtv = dtv.assign_coords(valid_time=dtv.valid_time + pd.Timedelta(hours=7))
# Slice by time
dtu = dtu.sel(valid_time=slice(sta_date, end_date))
dtv = dtv.sel(valid_time=slice(sta_date, end_date))

# Access variable
u10 = dtu["u10"]  
v10 = dtv["v10"]  

# Calculate w10
w10 = (u10*u10+v10*v10)**0.5
w10 = w10.assign_attrs(units="m/s", long_name="10m wind speed")

# Regrid using neareast method
new_lat = np.arange(min_lat, max_lat + reso, reso)
new_lon = np.arange(min_lon, max_lon + reso, reso)
op = w10.interp(latitude = new_lat, longitude = new_lon, method="nearest")

# Export output file
op.to_dataset(name="w10").to_netcdf(output_file, encoding = {"w10": {"zlib": True, "complevel": 4}})