import h5py
import numpy as np
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

AOD_DIR = PROJECT_DIR / "data" / "raw" / "AOD"
LST_DIR = PROJECT_DIR / "data" / "raw" / "LST"
DATA_DIR = PROJECT_DIR / "data" / "processed"

aod_file = AOD_DIR / "3DIMG_18JUN2024_0600_L2G_AOD_V02R00.h5"
lst_file = LST_DIR / "3DIMG_18JUN2024_0600_L2B_LST_V01R00.h5"

grid_size = 0.5

# Check input files
if not aod_file.exists():
    raise FileNotFoundError(f"AOD file not found: {aod_file}")

if not lst_file.exists():
    raise FileNotFoundError(f"LST file not found: {lst_file}")


# --------------------------------------------------
# 1. READ AOD
# --------------------------------------------------

with h5py.File(aod_file, "r") as f:

    aod = f["AOD"][:][0]
    latitude = f["latitude"][:]
    longitude = f["longitude"][:]
    time_value = f["time"][0]

# Convert fill value to NaN
aod = np.where(aod == -999, np.nan, aod)

# Create coordinate grids
lat_grid, lon_grid = np.meshgrid(
    latitude,
    longitude,
    indexing="ij"
)

# Flatten
aod_flat = aod.flatten()
lat_flat = lat_grid.flatten()
lon_flat = lon_grid.flatten()

# Keep valid AOD
valid = ~np.isnan(aod_flat)

aod_lat_valid = lat_flat[valid]
aod_lon_valid = lon_flat[valid]
aod_value_valid = aod_flat[valid]

print("Valid AOD observations:", len(aod_value_valid))


# --------------------------------------------------
# 2. CREATE AOD REGIONAL CELLS
# --------------------------------------------------

aod_cell_lat = np.floor(
    aod_lat_valid / grid_size
).astype(int)

aod_cell_lon = np.floor(
    aod_lon_valid / grid_size
).astype(int)

aod_df = pd.DataFrame({
    "cell_lat": aod_cell_lat,
    "cell_lon": aod_cell_lon,
    "AOD": aod_value_valid
})


# --------------------------------------------------
# 3. AGGREGATE AOD
# --------------------------------------------------

aod_regional = (
    aod_df
    .groupby(["cell_lat", "cell_lon"])
    .agg(
        AOD_mean=("AOD", "mean"),
        AOD_median=("AOD", "median"),
        AOD_std=("AOD", "std"),
        AOD_count=("AOD", "count")
    )
    .reset_index()
)


# --------------------------------------------------
# 4. READ LST
# --------------------------------------------------

with h5py.File(lst_file, "r") as f:

    lst = f["LST"][:][0]

    lat_raw = f["Latitude"][:]
    lon_raw = f["Longitude"][:]

# Apply coordinate scale factor
lst_lat = lat_raw.astype(float) * 0.01
lst_lon = lon_raw.astype(float) * 0.01

# Convert invalid LST values
lst = np.where(lst == -999, np.nan, lst)

# Invalid coordinate values
lst_lat = np.where(lat_raw == 32767, np.nan, lst_lat)
lst_lon = np.where(lon_raw == 32767, np.nan, lst_lon)


# --------------------------------------------------
# 5. RESTRICT LST TO AOD GEOGRAPHIC REGION
# --------------------------------------------------

region_mask = (
    (lst_lat >= -9.95) &
    (lst_lat <= 45.05) &
    (lst_lon >= 45.05) &
    (lst_lon <= 100.05)
)

valid_lst = (
    ~np.isnan(lst) &
    ~np.isnan(lst_lat) &
    ~np.isnan(lst_lon) &
    region_mask
)

lst_lat_region = lst_lat[valid_lst]
lst_lon_region = lst_lon[valid_lst]
lst_value_region = lst[valid_lst]

print(
    "Valid LST observations in AOD region:",
    len(lst_value_region)
)


# --------------------------------------------------
# 6. CREATE LST REGIONAL CELLS
# --------------------------------------------------

lst_cell_lat = np.floor(
    lst_lat_region / grid_size
).astype(int)

lst_cell_lon = np.floor(
    lst_lon_region / grid_size
).astype(int)

lst_df = pd.DataFrame({
    "cell_lat": lst_cell_lat,
    "cell_lon": lst_cell_lon,
    "LST": lst_value_region
})


# --------------------------------------------------
# 7. AGGREGATE LST
# --------------------------------------------------

lst_regional = (
    lst_df
    .groupby(["cell_lat", "cell_lon"])
    .agg(
        LST_mean=("LST", "mean"),
        LST_median=("LST", "median"),
        LST_std=("LST", "std"),
        LST_count=("LST", "count")
    )
    .reset_index()
)


# --------------------------------------------------
# 8. MERGE AOD + LST
# --------------------------------------------------

regional_df = pd.merge(
    aod_regional,
    lst_regional,
    on=["cell_lat", "cell_lon"],
    how="inner"
)


# --------------------------------------------------
# 9. DATA SUFFICIENCY FILTER
# --------------------------------------------------

regional_df = regional_df[
    (regional_df["AOD_count"] >= 5) &
    (regional_df["LST_count"] >= 10)
].copy()


# --------------------------------------------------
# 10. CREATE REGIONAL CENTRE
# --------------------------------------------------

regional_df["latitude"] = (
    regional_df["cell_lat"] * grid_size
    + grid_size / 2
)

regional_df["longitude"] = (
    regional_df["cell_lon"] * grid_size
    + grid_size / 2
)


# --------------------------------------------------
# 11. TIME
# --------------------------------------------------

regional_df["time"] = pd.Timestamp(
    "2024-06-18 06:00:00"
)


# --------------------------------------------------
# 12. FINAL COLUMN ORDER
# --------------------------------------------------

regional_df = regional_df[
    [
        "latitude",
        "longitude",
        "time",
        "AOD_mean",
        "AOD_median",
        "AOD_std",
        "AOD_count",
        "LST_mean",
        "LST_median",
        "LST_std",
        "LST_count"
    ]
].reset_index(drop=True)


# --------------------------------------------------
# 13. SAVE
# --------------------------------------------------

regional_df.to_csv(
    DATA_DIR / "regional_AOD_LST_0600.csv",
    index=False
)


# --------------------------------------------------
# 14. RESULTS
# --------------------------------------------------

print("\nFinal regional dataset shape:")
print(regional_df.shape)

print("\nFirst 10 rows:")
print(regional_df.head(10))

print("\nSummary:")
print(regional_df.describe())