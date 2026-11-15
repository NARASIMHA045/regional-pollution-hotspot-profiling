import h5py
import numpy as np
from pathlib import Path

# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

AOD_DIR = PROJECT_DIR / "data" / "raw" / "AOD"
LST_DIR = PROJECT_DIR / "data" / "raw" / "LST"

aod_file = AOD_DIR / "3DIMG_18JUN2024_0530_L2G_AOD_V02R00.h5"
lst_file = LST_DIR / "3DIMG_18JUN2024_0530_L2B_LST_V01R00.h5"


# =====================================================
# AOD
# =====================================================

with h5py.File(aod_file, "r") as f:

    aod = f["AOD"][0]
    aod_lat = f["latitude"][:]
    aod_lon = f["longitude"][:]

    aod_valid = aod != -999

    print("=" * 60)
    print("AOD GRID")
    print("=" * 60)

    print("AOD shape:", aod.shape)

    print("Latitude shape:", aod_lat.shape)
    print("Longitude shape:", aod_lon.shape)

    print("Latitude range:",
          aod_lat.min(),
          "to",
          aod_lat.max())

    print("Longitude range:",
          aod_lon.min(),
          "to",
          aod_lon.max())

    print("\nLatitude spacing:")
    print(np.unique(np.round(np.diff(aod_lat), 5))[:20])

    print("\nLongitude spacing:")
    print(np.unique(np.round(np.diff(aod_lon), 5))[:20])


# =====================================================
# LST
# =====================================================

with h5py.File(lst_file, "r") as f:

    lst = f["LST"][0]

    lst_lat_raw = f["Latitude"][:]
    lst_lon_raw = f["Longitude"][:]

    lst_lat = lst_lat_raw.astype(float) * 0.01
    lst_lon = lst_lon_raw.astype(float) * 0.01

    lst_valid_coordinates = (
        (lst_lat_raw != 32767) &
        (lst_lon_raw != 32767)
    )

    print("\n" + "=" * 60)
    print("LST GRID")
    print("=" * 60)

    print("LST shape:", lst.shape)

    print("Latitude shape:", lst_lat.shape)
    print("Longitude shape:", lst_lon.shape)

    valid_lat = lst_lat[lst_valid_coordinates]
    valid_lon = lst_lon[lst_valid_coordinates]

    print("Latitude range:",
          valid_lat.min(),
          "to",
          valid_lat.max())

    print("Longitude range:",
          valid_lon.min(),
          "to",
          valid_lon.max())


# =====================================================
# SAMPLE AOD LOCATIONS
# =====================================================

print("\n" + "=" * 60)
print("AOD SAMPLE LOCATIONS")
print("=" * 60)

sample_positions = [
    (0, 0),
    (100, 100),
    (200, 200),
    (300, 300),
    (400, 400),
    (500, 500)
]

for i, j in sample_positions:

    print(
        f"AOD[{i},{j}] → "
        f"Lat={aod_lat[i]:.2f}, "
        f"Lon={aod_lon[j]:.2f}, "
        f"AOD={aod[i,j]}"
    )


# =====================================================
# LST GRID SPACING
# =====================================================

print("\n" + "=" * 60)
print("LST GRID SPACING")
print("=" * 60)

# Choose a valid region around the center
i = 1000
j = 1000

print("\nReference pixel:")
print(f"Row = {i}, Column = {j}")

print(
    f"Latitude = {lst_lat[i,j]:.4f}, "
    f"Longitude = {lst_lon[i,j]:.4f}"
)


# -----------------------------------------------------
# Move horizontally: same row, different columns
# -----------------------------------------------------

print("\nHorizontal movement (changing column):")

for col in range(j, j + 5):

    print(
        f"[{i}, {col}] → "
        f"Lat = {lst_lat[i,col]:.4f}, "
        f"Lon = {lst_lon[i,col]:.4f}"
    )


# -----------------------------------------------------
# Move vertically: same column, different rows
# -----------------------------------------------------

print("\nVertical movement (changing row):")

for row in range(i, i + 5):

    print(
        f"[{row}, {j}] → "
        f"Lat = {lst_lat[row,j]:.4f}, "
        f"Lon = {lst_lon[row,j]:.4f}"
    )


# -----------------------------------------------------
# Calculate differences
# -----------------------------------------------------

print("\nHorizontal coordinate differences:")

for col in range(j, j + 4):

    lat_diff = lst_lat[i,col+1] - lst_lat[i,col]
    lon_diff = lst_lon[i,col+1] - lst_lon[i,col]

    print(
        f"Column {col} → {col+1}: "
        f"ΔLat = {lat_diff:.4f}, "
        f"ΔLon = {lon_diff:.4f}"
    )


print("\nVertical coordinate differences:")

for row in range(i, i + 4):

    lat_diff = lst_lat[row+1,j] - lst_lat[row,j]
    lon_diff = lst_lon[row+1,j] - lst_lon[row,j]

    print(
        f"Row {row} → {row+1}: "
        f"ΔLat = {lat_diff:.4f}, "
        f"ΔLon = {lon_diff:.4f}"
    )


# =====================================================
# AOD METADATA
# =====================================================

with h5py.File(aod_file, "r") as f:

    print("=" * 60)
    print("AOD METADATA")
    print("=" * 60)

    for dataset_name in ["AOD", "latitude", "longitude", "time"]:

        dataset = f[dataset_name]

        print(f"\nDataset: {dataset_name}")
        print("Shape:", dataset.shape)
        print("Data type:", dataset.dtype)

        print("Attributes:")

        for key, value in dataset.attrs.items():
            print(f"    {key}: {value}")