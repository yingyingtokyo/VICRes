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
sta_year = 2005
end_year = 2020

# Directories
main_dir = os.getcwd()
input_dir = os.path.join(main_dir, "download", "precipitation")  
output_file = os.path.join(main_dir, "preprocess", "chirps2_precip_2005-2020.nc")

# -------------------- Load daily data --------------------
print("Processing daily precipitation data: START")
prec_list = []
for year in range(sta_year, end_year+1):
    print(f"Year: {year}")
    file_name = f"chirps-v2.0.{year}.days_p05.nc"
    file_path = os.path.join(input_dir, file_name)
    
    # Open NetCDF and slice spatial domain
    with xr.open_dataset(file_path) as data:
        sliced = data.sel(latitude=slice(min_lat-5, max_lat+5),
                          longitude=slice(min_lon-5, max_lon+5))
        prec_list.append(sliced)

# Concatenate all years along time
prec_daily = xr.concat(prec_list, dim="time")
print("Processing daily precipitation data: DONE")

# -------------------- Convert to 6-hourly --------------------
print("Converting daily to 6-hourly precipitation: START")
daily_prec = prec_daily['precip']

# Create 6-hourly time index
start = daily_prec.time.min().values
end = daily_prec.time.max().values
time_6h = pd.date_range(start=start, end=end + np.timedelta64(18, 'h'), freq='6H')

# Create 6-hourly array filled with zeros
data_6h = xr.DataArray(
    np.zeros((len(time_6h), daily_prec.latitude.size, daily_prec.longitude.size), dtype=np.float32),
    coords={'time': time_6h, 'latitude': daily_prec.latitude, 'longitude': daily_prec.longitude},
    dims=['time', 'latitude', 'longitude']
)

# Assign daily value to 18:00 of each day
# Vectorized approach
time_6h_array = np.array(time_6h)
daily_time_array = np.array(daily_prec.time.values, dtype='datetime64[D]')  # daily dates

# Compute indices for 18:00 of each day
indices_18h = np.searchsorted(time_6h_array, daily_time_array + np.timedelta64(18, 'h'))

# Assign values
data_6h[indices_18h, :, :] = daily_prec.values

# Wrap into dataset
prec_6h = xr.Dataset({'precip': data_6h})
print("Converting daily to 6-hourly precipitation: DONE")
print(prec_6h)

# Regrid data using neareast method
new_lat = np.arange(min_lat, max_lat + reso, reso)
new_lon = np.arange(min_lon, max_lon + reso, reso)
op = prec_6h.interp(latitude = new_lat, longitude = new_lon, method="nearest")

# Export output file
op.to_netcdf(output_file)
print("Precipitation data process: DONE")