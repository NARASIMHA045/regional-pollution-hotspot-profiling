import h5py
import numpy as np
import pandas as pd
from pathlib import Path

# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
LST_DIR = PROJECT_DIR / "data" / "raw" / "LST"

file_path = LST_DIR / "3DIMG_18JUN2024_0530_L2B_LST_V01R00.h5"


# =====================================================
# READ LST DATA
# =====================================================

with h5py.File(file_path, "r") as f:

    lst = f["LST"][0]
    latitude = f["Latitude"][:]
    longitude = f["Longitude"][:]
    time_value = f["time"][0]

    print("LST shape:", lst.shape)

    print("\nLST raw values:")
    print("Minimum:", np.min(lst))
    print("Maximum:", np.max(lst))

    print("\nMissing values:")
    print("-999 count:", np.sum(lst == -999))

    valid_lst = lst[lst != -999]

    print("Valid count:", len(valid_lst))
    print("Valid minimum:", np.min(valid_lst))
    print("Valid maximum:", np.max(valid_lst))

    print("\nLatitude:")
    print("Shape:", latitude.shape)
    print("Raw minimum:", np.min(latitude))
    print("Raw maximum:", np.max(latitude))

    print("\nLongitude:")
    print("Shape:", longitude.shape)
    print("Raw minimum:", np.min(longitude))
    print("Raw maximum:", longitude.max())

    observation_time = (
        pd.Timestamp("2000-01-01")
        + pd.to_timedelta(time_value, unit="m")
    )

    print("\nTime value:", time_value)
    print("Observation time:", observation_time)