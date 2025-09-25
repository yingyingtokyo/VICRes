# Libraries
import os           # For handling file paths
import pandas as pd # For handling tabular data (VIC input/output)
import xarray as xr # For working with NetCDF climate data

# Directories
main_dir = os.getcwd()
input_dir = os.path.join(main_dir, "preprocess")  
output_dir = os.path.join(main_dir, "vic_inp_acsii") 

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


# EXTRACTING AND WRITING OUT DATA FOR VIC _____________________________________
print("Extracting and writing out data for VIC: START")

# Load locations (longitude, latitude) where VIC input files are needed
loc = pd.read_csv("lon_lat.txt", sep="\t", header=None, names=["lon", "lat"])

# Loop over each location
for index, row in loc.iterrows():
    lon = row['lon']
    lat = row['lat']
    print("lat: "+str(lat)+", lon: "+str(lon))    
    
    # Extract the nearest grid point data for each variable
    sel_prec = prec["precip"].sel(latitude=lat, longitude=lon, method="nearest")
    sel_temp = temp["t2m"].sel(latitude=lat, longitude=lon, method="nearest")
    sel_sdswrf = sdswrf["avg_sdswrf"].sel(latitude=lat, longitude=lon, method="nearest")
    sel_sdlwrf = sdlwrf["avg_sdlwrf"].sel(latitude=lat, longitude=lon, method="nearest")    
    sel_sp = sp["sp"].sel(latitude=lat, longitude=lon, method="nearest")    
    sel_vp = vp["vp"].sel(latitude=lat, longitude=lon, method="nearest")         
    sel_wind = wind["w10"].sel(latitude=lat, longitude=lon, method="nearest")   
    
    # Create a pandas DataFrame with VIC-required variables
    df = pd.DataFrame({
        "prec": sel_prec.values,        # Precipitation (mm/day)
        "temp": sel_temp.values,        # Temperature °C
        "sdswrf": sel_sdswrf.values,    # Shortwave Radiation (W/m2)
        "sdlwrf": sel_sdlwrf.values,    # Longwave Radiation (W/m2)                
        "sp": sel_sp.values,            # Atmosphere Pressure (kPa)        
        "vp": sel_vp.values,            # Vapor Pressure (kPa)           
        "wind": sel_wind.values         # Wind speed (m/s)
    })

    # Define output filename and write to file (tab-separated, no header/index)
    filename = f"gf_{lon:.4f}_{lat:.4f}"  # Original format, no .txt extension
    file_path = os.path.join(output_dir, filename)
    df.to_csv(file_path, sep="\t", index=False, header=False, float_format="%.6f")
    
print("Extracting and writing out data for VIC: DONE")