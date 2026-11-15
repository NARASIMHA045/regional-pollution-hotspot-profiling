import h5py
import numpy as np
from pathlib import Path

# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
LST_DIR = PROJECT_DIR / "data" / "raw" / "LST"

file_path = LST_DIR / "3DIMG_18JUN2024_0530_L2B_LST_V01R00.h5"


# =====================================================
# INSPECT LST FILE STRUCTURE
# =====================================================

with h5py.File(file_path, "r") as f:

    print("Datasets in LST file:")
    print("----------------------")

    def show_structure(name, obj):
        if isinstance(obj, h5py.Dataset):
            print(f"\nDataset: {name}")
            print("Shape:", obj.shape)
            print("Data type:", obj.dtype)

            print("Attributes:")
            for key, value in obj.attrs.items():
                print(f"    {key}: {value}")

    f.visititems(show_structure)


# =====================================================
# INSPECT LATITUDE AND LONGITUDE
# =====================================================

with h5py.File(file_path, "r") as f:

    latitude_raw = f["Latitude"][:]
    longitude_raw = f["Longitude"][:]

    # Fill value
    fill_value = 32767

    # Remove missing coordinates
    latitude_valid = latitude_raw[latitude_raw != fill_value]
    longitude_valid = longitude_raw[longitude_raw != fill_value]

    # Apply scale factor
    latitude = latitude_valid * 0.01
    longitude = longitude_valid * 0.01

    print("LATITUDE")
    print("--------")
    print("Valid count:", len(latitude))
    print("Minimum:", np.min(latitude))
    print("Maximum:", np.max(latitude))
    print("First 10:", latitude[:10])
    print("Last 10:", latitude[-10:])

    print("\nLONGITUDE")
    print("---------")
    print("Valid count:", len(longitude))
    print("Minimum:", np.min(longitude))
    print("Maximum:", np.max(longitude))
    print("First 10:", longitude[:10])
    print("Last 10:", longitude[-10:])


# =====================================================
# COORDINATE SAMPLES AT SPECIFIC PIXELS
# =====================================================

print("\nCoordinate samples at specific pixels")
print("--------------------------------------")

positions = [
    (0, 0),
    (0, 1000),
    (1000, 1000),
    (2000, 1000),
    (2815, 2804)
]

for i, j in positions:

    lat_raw = latitude_raw[i, j]
    lon_raw = longitude_raw[i, j]

    if lat_raw == fill_value or lon_raw == fill_value:
        print(f"Pixel ({i}, {j}) → Missing coordinate")

    else:
        lat = lat_raw * 0.01
        lon = lon_raw * 0.01

        print(
            f"Pixel ({i}, {j}) → "
            f"Latitude: {lat:.2f}, "
            f"Longitude: {lon:.2f}"
        )