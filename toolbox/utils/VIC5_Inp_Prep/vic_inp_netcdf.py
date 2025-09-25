# Libraries
import os           # For handling file paths
import xarray as xr # For working with NetCDF climate data

# Directories
main_dir = os.getcwd()
input_dir = os.path.join(main_dir, "preprocess")  
output_dir = os.path.join(main_dir, "vic_inp_netcdf") 

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)


# PROCESSING __________________________________________________________________

# -------------------- Precipitation --------------------
print("Loading precipitation data")
file_name = "chirps2_precip_2005-2020.nc"
file_path = os.path.join(input_dir, file_name)
prec = xr.open_dataset(file_path)

# -------------------- Temperature --------------------
print("Loading temperature data")
file_name = "era5_t2m_2005-2020.nc"
file_path = os.path.join(input_dir, file_name)
temp = xr.open_dataset(file_path)

# -------------------- Shortwave Radiation --------------------
print("Loading shortwave radiation data")
file_name = "era5_sdswrf_2005-2020.nc"
file_path = os.path.join(input_dir, file_name)
sdswrf = xr.open_dataset(file_path)

# -------------------- Longwave Radiation --------------------
print("Loading shortwave radiation data")
file_name = "era5_sdlwrf_2005-2020.nc"
file_path = os.path.join(input_dir, file_name)
sdlwrf = xr.open_dataset(file_path)

# -------------------- Atmosphere Pressure --------------------
print("Loading atmosphere pressure data")
file_name = "era5_sp_2005-2020.nc"
file_path = os.path.join(input_dir, file_name)
sp = xr.open_dataset(file_path)

# -------------------- Vapor Pressure --------------------
print("Loading vapor pressure data")
file_name = "era5_vp_2005-2020.nc"
file_path = os.path.join(input_dir, file_name)
vp = xr.open_dataset(file_path)

# -------------------- Wind Speed --------------------
print("Loading windspeed data")
file_name = "era5_w10_2005-2020.nc"
file_path = os.path.join(input_dir, file_name)
wind = xr.open_dataset(file_path)


# Merge all datasets along common dimensions (e.g., time, lat, lon)
print("Merging datasets")
dt = xr.merge([prec, temp, sdswrf, sdlwrf, sp, vp, wind])

# Export output file
print("Saving merged dataset")
output_file = os.path.join(output_dir, "vic_inp_2005-2020.nc")
dt.to_netcdf(output_file)
print("Completed")