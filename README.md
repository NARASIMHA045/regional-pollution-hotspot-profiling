# Regional Pollution Hotspot Profiles from Satellite-Derived Environmental Features
### 🚀 Live Dashboard

**Explore the deployed application:**  
https://regional-pollution-hotspot-profiling.streamlit.app

**GitHub Repository:**  
https://github.com/NARASIMHA045/regional-pollution-hotspot-profiling

### 📸 Dashboard Preview

![Regional Pollution Hotspot Dashboard](screenshots/dashboard.png)

## 1. Project Overview

This project explores regional environmental patterns using satellite-derived data from the INSAT-3D satellite.

It combines Aerosol Optical Depth (AOD) and Land Surface Temperature (LST) to identify and profile regions with different environmental characteristics using unsupervised machine learning.

The project applies K-Means clustering to group regional observations based on their aerosol loading and land surface temperature.

An interactive Streamlit dashboard is developed to visualize the resulting regional clusters.

## 2. Objectives

- Process satellite-derived environmental datasets.
- Prepare regional observations using a 0.5° × 0.5° spatial grid.
- Analyze the relationship between Aerosol Optical Depth and Land Surface Temperature.
- Apply K-Means clustering to identify groups with similar environmental characteristics.
- Evaluate clustering performance using multiple evaluation metrics.
- Visualize regional cluster distributions through maps and plots.

## 3. Data Sources

The primary satellite data used in this project comes from INSAT-3D products obtained through MOSDAC.

| Dataset | Description |
|---|---|
| AOD | Aerosol Optical Depth |
| LST | Land Surface Temperature |
| Smoke | Supplementary smoke-related data |
| Fire | Supplementary fire-related data |
| Rainfall | Supplementary rainfall analysis |

Geographical boundary data is used for regional map visualization.

## 4. Methodology

### Step 1: Data Preparation
- Read satellite data.
- Handle missing and invalid values.
- Extract relevant geographical and environmental features.
- Prepare regional observations.

### Step 2: Spatial Aggregation
- Divide the study region into 0.5° × 0.5° grid cells.
- Aggregate satellite observations within each grid cell.
- Prepare regional AOD and LST features.

### Step 3: Data Preprocessing
- Select relevant numerical features.
- Standardize features before clustering.

### Step 4: Clustering
- Apply K-Means clustering.
- Experiment with different cluster counts.
- Compare Euclidean and Manhattan distance-based evaluation approaches where applicable.

### Step 5: Cluster Evaluation
Evaluate clustering results using:
- Within-Cluster Sum of Squares (WCSS)
- Silhouette Score
- Davies-Bouldin Index
- Adjusted Rand Index for applicable comparisons

### Step 6: Visualization
- Visualize clusters using Principal Component Analysis (PCA).
- Generate AOD versus LST cluster plots.
- Display regional cluster distributions on geographical maps.

## 5. Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- SciPy
- Scikit-learn
- GeoPandas
- Folium
- Streamlit
- HDF5

## 6. Project Structure

```text
Project/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   │   ├── AOD/
│   │   ├── Fire/
│   │   ├── Rainfall/
│   │   └── Smoke/
│   │
│   └── processed/
│       ├── clustered_regional_dataset_0530.csv
│       ├── cluster_profiles_0530.csv
│       ├── cluster_summary_clean_0530.csv
│       ├── final_regional_dataset_0530.csv
│       ├── regional_AOD_LST_0530.csv
│       ├── regional_AOD_LST_0600.csv
│       ├── regional_Fire_0530.csv
│       ├── regional_Rainfall_0530.csv
│       └── regional_Smoke_0530.csv
│
├── map_boundaries/
│
├── notebooks/
│   ├── 01_AOD_Data_Preparation.ipynb
│   ├── 02_Clustering_Analysis.ipynb
│   ├── 530_rainfall.ipynb
│   ├── inspect_time6.ipynb
│   └── kdTree.ipynb
│
├── results/
│   ├── AOD_vs_LST_clusters_0530.png
│   └── regional_cluster_map_0530.png
│
└── scripts/
    ├── compare_grids.py
    ├── ins.py
    ├── inspect_hdf.py
    ├── inspect_LST.py
    └── time6.py
```

## 7. Running the Project

### Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

### Navigate to the project directory

```bash
cd "Regional Pollution Hotspot Profiles from Satellite-Derived Environmental Features"
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the dashboard

```bash
streamlit run app.py
```

## 8. Limitations

- Aerosol Optical Depth is a column-integrated aerosol measurement and is not a direct measurement of ground-level PM2.5 or AQI.
- Land Surface Temperature represents the temperature of the land surface, not near-surface air temperature.
- The current clustering analysis uses AOD and LST as its primary features.
- The analysis of a single observation date and time cannot establish persistent pollution hotspots or long-term trends.
- Satellite observations may contain missing values and spatial coverage limitations.
- Additional ground-based air-quality measurements would be needed to validate relationships with actual surface-level pollution.

## 9. Future Improvements

- Integrate additional satellite-derived environmental variables.
- Expand the analysis across multiple dates and time periods.
- Explore spatial matching using KD-Tree.
- Investigate the contribution of rainfall, smoke and fire-related features.
- Compare additional clustering algorithms.
- Validate satellite-derived patterns using ground-based air-quality observations.
- Improve the dashboard with additional temporal and spatial analysis.

## 10. Project Status

The current implementation focuses on regional profiling using AOD and LST features, K-Means clustering, cluster evaluation and interactive visualization.

Additional environmental data processing and spatial analysis notebooks are retained for future development.