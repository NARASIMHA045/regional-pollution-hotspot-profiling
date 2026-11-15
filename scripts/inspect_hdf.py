import h5py
import numpy as np
from pathlib import Path

# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
AOD_DIR = PROJECT_DIR / "data" / "raw" / "AOD"

file_path = AOD_DIR / "3DIMG_18JUN2024_0530_L2G_AOD_V02R00.h5"


# =====================================================
# INSPECT HDF5 FILE STRUCTURE
# =====================================================

with h5py.File(file_path, "r") as f:

    print("FILE OPENED SUCCESSFULLY\n")

    for name in f:
        print("Dataset:", name)

        data = f[name]

        print("Shape:", data.shape)
        print("Data type:", data.dtype)

        print("Attributes:")

        for key, value in data.attrs.items():
            print("   ", key, ":", value)

        print("-" * 50)


# =====================================================
# INSPECT AOD DATA AND COORDINATES
# =====================================================

with h5py.File(file_path, "r") as f:

    aod = f["AOD"][:]
    lat = f["latitude"][:]
    lon = f["longitude"][:]
    time = f["time"][:]

    print("AOD shape:", aod.shape)

    print("\nLatitude:")
    print("Minimum:", lat.min())
    print("Maximum:", lat.max())
    print("First 5:", lat[:5])
    print("Last 5:", lat[-5:])

    print("\nLongitude:")
    print("Minimum:", lon.min())
    print("Maximum:", lon.max())
    print("First 5:", lon[:5])
    print("Last 5:", lon[-5:])

    print("\nAOD:")
    print("Minimum:", np.min(aod))
    print("Maximum:", np.max(aod))

    print("\nNumber of -999 values:", np.sum(aod == -999))

    print("\nTime value:", time)