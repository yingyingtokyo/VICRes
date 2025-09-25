***VIC5_Inp_Prep*** --- A Python-based Package for VIC 5.x Climate Input Preparation 
writen by Vu Trung Dung (dtvu2205@gmail.com)

________________________________________________________________________________

# Overview
This package provides a suite of Python scripts for preparing climate input data for the Variable Infiltration Capacity (VIC) hydrological model (version 5.x). It processes raw NetCDF-format climate datasets, regrids them to a predefined spatial grid, and exports the outputs in both ASCII format (for the classic VIC driver) and NetCDF format (for the image VIC driver). The package handles a range of essential climate variables, including precipitation, air temperature, shortwave radiation, longwave radiation, atmospheric pressure, vapor pressure, and wind speed. The package requires Python 3.x and depends on libraries such as numpy, pandas, xarray, netCDF4 or h5netcdf, os and math.

________________________________________________________________________________

# How to Use
1. Prepare Input Data
Download raw NetCDF files (e. g., CHIRPS2, ERA5) and organize downloaded data into the directory structure (see below).

2. Define Your Spatial Points
Create a text file named lon_lat.txt with your points of interest. The file is formatted as tab-separated columns of longitude and latitude, one point per line.

3. Run Preprocessing Scripts
***pre_precipitation.py***
***pre_temperature.py***
***pre_radiation.py***
***pre_atmosphere_pressure.py***
***pre_vapor_pressure.py***
***pre_wind_speed.py***
Note: adjust the spatial and temporal domain and spatial resolution in each script as desired.

4. Generate VIC Input Files
Once all climate variables are preprocessed:
For VIC Image Driver (NetCDF input), run vic_inp_netcdf.py. Output are stored in ***/vic_inp_netcdf***
For VIC Classic Driver (ASCII input), run vic_inp_ascii.py, output are stored in ***/vic_inp_ascii***

________________________________________________________________________________

# Directory Structure
```
base_dir/
├─ download/                        # Downloaded raw climate data (NetCDF format)
    ├─ atmosphere_pressure/	        # Atmosphere pressure data
    ├─ precipitation/               # Precipitation data
    ├─ radiation/                   # Radiation data (short-wave and long-wave)
    ├─ temperature/	                # Air and dew point temperature (for vapor pressure) data
    ├─ wind_speed/                  # Wind speed component (u and v) data 
├─ preprocess/                      # Preprocessed data, used to prepare climate input for VIC
    ├─ era5_sp_2005-2020.nc	        # Preprocessed atmospheric pressure data
    ├─ chirps2_precip_2005-2020.nc  # Preprocessed precipitation data
    ├─ era5_sdswrf_2005-2020.nc	    # Preprocessed short-wave radiation data
    ├─ era5_sdlwrf_2005-2020.nc 	# Preprocessed long-wave radiation data
    ├─ era5_t2m_2005-2020.nc		# Preprocessed air temperature data
    ├─ era5_vp_2005-2020.nc 		# Preprocessed vapor pressure datda
    ├─ era5_w10_2005-2020.nc		# Preprocessed wind speed data
├─ vic_inp_netcdf/                  # VIC climate input files in NetCDF format
    ├─ vic_inp_2005-2020.nc      
├─ vic_inp_ascii/                   # VIC climate input files in ASCII format
    ├─ gf_lon_lat                   # Files named by lon and lat (e.g., gf_93.9069_18.9189)
├─ lon_lat.txt                      # List of lon-lat points to extract VIC climate input flies
├─ pre_atmosphere_pressure.py       # Script for processing atmospheric pressure data
├─ pre_precipitation.py	            # Script for processing  precipitation data
├─ pre_radiation.py                 # Script for processing short-wave and long-wave radiation data
├─ pre_temperature.py               # Script for processing air temperature data
├─ pre_vapor_pressure.py            # Script for processing vapor pressure data
├─ pre_wind_speed.py                # Script for processing wind speed data
├─ vic_inp_netcdf.py                # Script for preparing VIC climate input files in NetCDF format
├─ vic_inp_ascii.py                 # Script for preparing VIC climate input files in ASCII format
```

________________________________________________________________________________

# Data Processing Workflow
1. Download raw climate datasets
Raw data files are stored in the ***/download*** directory.

2. Preprocess each climate variable separately
- Adjust time zones if necessary (e.g., shift by +7 hours for the Mekong region).
- Slice the data temporally (e.g., from 2005-01-01 to 2020-12-31).
- Calculate derived variables where needed (e.g., vapor pressure from dew point temperature, wind speed from u and v components).
- Convert units when required (e.g., temperature from Kelvin to Celsius).
- Re-grid spatially to a uniform resolution (e.g., 0.0625°).
- Save the preprocessed variables as separate NetCDF files in the /preprocess directory.

3. Prepare VIC climate input files in NetCDF format
Merge all preprocessed climate variables into one multi-variable NetCDF file stored in ***/vic_inp_netcdf***.

4. Prepare VIC climate input files in ASCII format
Extract time series for specified longitude-latitude points and save as ASCII files in ***/vic_inp_ascii***.

________________________________________________________________________________

# Script Explanation
1. Preprocessing Scripts
- ***pre_precipitation.py*** --- precipitation preprocessing
Inputs: Raw daily CHIRPS2 precipitation NetCDF files (***/download/precipitation/***)
Operations: Temporal slicing, daily to 6-hr data conversion, re-gridding
Output: ***chirps2_precip_2005-2020.nc*** saved in ***/preprocess***

- ***pre_temperature.py*** --- temperature preprocessing
Inputs: Raw 6-hr ERA5 temperature NetCDF files (***/download/temperature/***)
Operations: Time zone adjustment, temporal slicing, unit conversion (K → °C), re-gridding
Output: ***era5_t2m_2005-2020.nc*** saved in ***/preprocess***

- ***pre_radiation.py*** --- short-wave and long-wave Radiation preprocessing
Inputs: Raw 6-hr ERA5 short-wave and long-wave radiation NetCDF files (***/download/radiation/***)
Operations: Time zone adjustment, temporal slicing, re-gridding
Outputs: ***era5_sdswrf_2005-2020.nc*** (shortwave) and ***era5_sdlwrf_2005-2020.nc*** (longwave) saved in ***/preprocess***

- ***pre_atmosphere_pressure.py*** --- atmospheric pressure preprocessing
Inputs: Raw 6-hr ERA5 surface pressure NetCDF files (***/download/pressure/***)
Operations: Time zone adjustment, temporal slicing, re-gridding
Output: ***era5_sp_2005-2020.nc*** saved in ***/preprocess***

- ***pre_vapor_pressure.py*** --- vapor pressure preprocessing
Inputs: Raw 6-hr ERA5 dew point temperature NetCDF files (***/download/temperature/***)
Operations: Time zone adjustment, temporal slicing, unit conversion, vapor pressure calculation, re-gridding
 Output: ***era5_vp_2005-2020.nc*** saved in ***/preprocess***

- ***pre_wind_speed.py*** --- wind speed preprocessing
Inputs: Raw 6-hr ERA5 u10 and v10 wind components NetCDF files (***/download/wind_speed/***)
Operations: Time zone adjustment, temporal slicing, wind speed calculation, re-gridding
 Output: ***era5_w10_2005-2020.nc*** saved in ***/preprocess***

2. VIC Input Preparation Scripts
- ***vic_inp_netcdf.py*** --- NetCDF merging script
Inputs: Preprocessed NetCDF climate variable files from ***/preprocess***
Operations: Merge all climate variables into a single NetCDF file
Output: ***vic_inp_2005-2020.nc*** saved in ***/vic_inp_netcdf***

- ***vic_inp_ascii.py*** --- ASCII extraction script
Inputs: Preprocessed NetCDF climate variable files from ***/preprocess*** and list of locations (***lon_lat.txt***)
Operations: Extract nearest grid cell time series for each location, save as tab-separated ASCII files
Output: ASCII VIC input files saved in ***/vic_inp_ascii*** (filename format: ***gf_{lon}_{lat}***)

*--- end of documents ---*