import streamlit as st
import pandas as pd
import folium

from streamlit_folium import st_folium
from pathlib import Path


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Regional Pollution Hotspot Profiling",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data" / "processed"
RESULTS_DIR = BASE_DIR / "results"

DATA_FILE = DATA_DIR / "clustered_regional_dataset_0530.csv"
SUMMARY_FILE = DATA_DIR / "cluster_summary_clean_0530.csv"
SCATTER_FILE = RESULTS_DIR / "AOD_vs_LST_clusters_0530.png"


# ============================================================
# 3. LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    data = pd.read_csv(DATA_FILE)

    summary = None

    if SUMMARY_FILE.exists():
        summary = pd.read_csv(SUMMARY_FILE)

    return data, summary


if not DATA_FILE.exists():

    st.error(
        "Dataset not found: clustered_regional_dataset_0530.csv"
    )

    st.stop()


try:

    df, summary_df = load_data()

except Exception as error:

    st.error(f"Unable to load dataset: {error}")
    st.stop()


# ============================================================
# 4. VALIDATE DATA
# ============================================================

required_columns = [
    "AOD_mean",
    "LST_mean",
    "Cluster_K3"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(f"Missing required columns: {missing_columns}")
    st.stop()


for col in required_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )


df = df.dropna(
    subset=required_columns
).copy()

df["Cluster_K3"] = df["Cluster_K3"].astype(int)


# ============================================================
# 5. CLUSTER CONFIGURATION
# ============================================================

CLUSTER_COLORS = {
    0: "#E76F51",
    1: "#2878B5",
    2: "#239B75"
}

available_clusters = sorted(
    df["Cluster_K3"].unique()
)


def get_cluster_name(cluster):

    return f"Cluster {int(cluster)}"


def get_cluster_color(cluster):

    return CLUSTER_COLORS.get(
        int(cluster),
        "#777777"
    )


def get_cluster_statistics(cluster):

    data = df[
        df["Cluster_K3"] == cluster
    ]

    count = len(data)

    percentage = (
        count / len(df) * 100
        if len(df) > 0 else 0
    )

    return {
        "count": count,
        "percentage": percentage,
        "aod": data["AOD_mean"].mean(),
        "lst": data["LST_mean"].mean()
    }


# ============================================================
# 6. FIND COORDINATE COLUMNS
# ============================================================

def find_column(possible_names):

    for column in possible_names:

        if column in df.columns:
            return column

    return None


latitude_col = find_column([
    "latitude",
    "Latitude",
    "LATITUDE",
    "lat",
    "Lat",
    "LAT"
])

longitude_col = find_column([
    "longitude",
    "Longitude",
    "LONGITUDE",
    "lon",
    "Lon",
    "LON",
    "lng"
])


# ============================================================
# 7. SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🌍 Environmental Explorer")

    st.caption(
        "Regional Satellite-Derived Analysis"
    )

    st.divider()

    st.subheader("AOD Filter")

    min_aod = float(df["AOD_mean"].min())
    max_aod = float(df["AOD_mean"].max())

    selected_aod = st.slider(
        "Select AOD range",
        min_value=min_aod,
        max_value=max_aod,
        value=(min_aod, max_aod),
        step=0.01,
        format="%.2f"
    )

    st.caption(
        f"Selected range: {selected_aod[0]:.2f} – "
        f"{selected_aod[1]:.2f}"
    )

    st.divider()

    st.subheader("Cluster Legend")

    for cluster in available_clusters:

        color = get_cluster_color(cluster)

        st.markdown(
            f"<span style='color:{color}'>●</span> "
            f"{get_cluster_name(cluster)}",
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader("Project Information")

    st.write("**Satellite:** INSAT-3D")
    st.write("**Data Portal:** MOSDAC")
    st.write("**Algorithm:** K-Means")
    st.write("**Observation Date:** 18 June 2024")
    st.write("**Observation Time:** 05:30")


# ============================================================
# 8. FILTER DATA
# ============================================================

filtered_df = df[
    (df["AOD_mean"] >= selected_aod[0]) &
    (df["AOD_mean"] <= selected_aod[1])
].copy()


# ============================================================
# 9. MAIN HEADER
# ============================================================

st.title("🌍 Regional Pollution Hotspot Profiling")

st.caption(
    "Satellite-Derived Environmental Intelligence Dashboard"
)

st.info(
    """
    **Observation Period:** 18 June 2024 | 05:30

    This dashboard explores regional environmental profiles
    using Aerosol Optical Depth (AOD) and Land Surface
    Temperature (LST).

    **Note:** The identified clusters represent preliminary
    environmental profiles, not confirmed ground-level
    pollution hotspots.
    """
)


# ============================================================
# 10. ENVIRONMENTAL OVERVIEW
# ============================================================

st.header("Environmental Overview")

st.caption(
    "Key statistics from the regional dataset."
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        label="Total Regions",
        value=f"{len(df):,}"
    )

with col2:

    st.metric(
        label="Clusters Identified",
        value=len(available_clusters)
    )

with col3:

    st.metric(
        label="Average AOD",
        value=f"{df['AOD_mean'].mean():.3f}"
    )

with col4:

    st.metric(
        label="Average LST",
        value=f"{df['LST_mean'].mean():.2f} K"
    )


# ============================================================
# 11. REGIONAL CLUSTER PROFILES
# ============================================================

st.header("Regional Cluster Profiles")

st.caption(
    "Environmental characteristics of the identified clusters."
)

cluster_columns = st.columns(
    len(available_clusters)
)

for index, cluster in enumerate(available_clusters):

    stats = get_cluster_statistics(cluster)

    color = get_cluster_color(cluster)

    with cluster_columns[index]:

        with st.container(border=True):

            st.markdown(
                f"### :material/circle: {get_cluster_name(cluster)}"
            )

            st.metric(
                "Regional Observations",
                stats["count"]
            )

            st.write(
                f"**Distribution:** {stats['percentage']:.2f}%"
            )

            st.write(
                f"**Mean AOD:** {stats['aod']:.3f}"
            )

            st.write(
                f"**Mean LST:** {stats['lst']:.2f} K"
            )


st.divider()


# ============================================================
# 12. DASHBOARD TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🗺️ Geographical Analysis",
    "📁 Regional Data",
    "ℹ️ Methodology"
])


# ============================================================
# TAB 1: OVERVIEW
# ============================================================

with tab1:

    st.subheader("Cluster Comparison")

    st.caption(
        "Comparison of average AOD and LST across clusters."
    )

    comparison = (
        df.groupby("Cluster_K3")
        [["AOD_mean", "LST_mean"]]
        .mean()
        .reset_index()
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("#### Average AOD")

        aod_chart = comparison.set_index(
            "Cluster_K3"
        )[["AOD_mean"]]

        st.bar_chart(aod_chart)

    with col2:

        st.markdown("#### Average LST")

        lst_chart = comparison.set_index(
            "Cluster_K3"
        )[["LST_mean"]]

        st.bar_chart(lst_chart)

    st.divider()

    st.subheader("Cluster Distribution")

    distribution = (
        df["Cluster_K3"]
        .value_counts()
        .sort_index()
    )

    st.bar_chart(distribution)

    st.divider()

    st.subheader("AOD vs LST Cluster Visualization")

    st.caption(
        "Relationship between Aerosol Optical Depth "
        "and Land Surface Temperature."
    )

    if SCATTER_FILE.exists():

        st.image(
            str(SCATTER_FILE),
            use_container_width=True
        )

    else:

        st.warning(
            "AOD_vs_LST_clusters_0530.png was not found."
        )

    st.divider()

    st.subheader("Cluster Summary")

    if summary_df is not None:

        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Cluster summary file is unavailable."
        )


# ============================================================
# TAB 2: GEOGRAPHICAL ANALYSIS
# ============================================================

with tab2:

    st.header("Geographical Analysis")

    st.write(
        "Explore the geographical distribution of "
        "the 430 regional observations and their clusters."
    )

    # --------------------------------------------------------
    # STEP 1: CHECK COORDINATE COLUMNS
    # --------------------------------------------------------

    latitude_col = "latitude"
    longitude_col = "longitude"

    if latitude_col not in df.columns or longitude_col not in df.columns:

        st.error("Latitude or longitude columns are missing.")

        st.write("Available dataset columns:")
        st.write(df.columns.tolist())

        st.stop()

    # --------------------------------------------------------
    # STEP 2: PREPARE MAP DATA
    # --------------------------------------------------------

    map_df = filtered_df.copy()

    map_df[latitude_col] = pd.to_numeric(
        map_df[latitude_col],
        errors="coerce"
    )

    map_df[longitude_col] = pd.to_numeric(
        map_df[longitude_col],
        errors="coerce"
    )

    map_df = map_df.dropna(
        subset=[
            latitude_col,
            longitude_col,
            "AOD_mean",
            "LST_mean",
            "Cluster_K3"
        ]
    )

    # Validate coordinates

    map_df = map_df[
        map_df[latitude_col].between(-90, 90) &
        map_df[longitude_col].between(-180, 180)
    ].copy()

    # --------------------------------------------------------
    # STEP 3: DISPLAY STATISTICS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Regional Observations",
            len(df)
        )

    with col2:

        st.metric(
            "Filtered Observations",
            len(filtered_df)
        )

    with col3:

        st.metric(
            "Locations Available on Map",
            len(map_df)
        )

    st.divider()

    # --------------------------------------------------------
    # STEP 4: DISPLAY MAP
    # --------------------------------------------------------

    st.subheader("Regional Cluster Distribution Map")

    if map_df.empty:

        st.error(
            "No valid geographical observations found. "
            "Check the latitude and longitude values."
        )

        st.write(
            df[[
                "latitude",
                "longitude",
                "AOD_mean",
                "LST_mean",
                "Cluster_K3"
            ]].head(10)
        )

    else:

        center_lat = map_df["latitude"].mean()
        center_lon = map_df["longitude"].mean()

        regional_map = folium.Map(
            location=[
                center_lat,
                center_lon
            ],
            zoom_start=5,
            tiles="OpenStreetMap"
        )

        # ----------------------------------------------------
        # ADD CLUSTER MARKERS
        # ----------------------------------------------------

        cluster_colors = {
            0: "#E76F51",
            1: "#2878B5",
            2: "#239B75"
        }

        for _, row in map_df.iterrows():

            cluster = int(row["Cluster_K3"])

            color = cluster_colors.get(
                cluster,
                "#777777"
            )

            popup_text = f"""
            <b>Cluster:</b> {cluster}<br>
            <b>AOD:</b> {row['AOD_mean']:.3f}<br>
            <b>LST:</b> {row['LST_mean']:.2f} K<br>
            <b>Latitude:</b> {row['latitude']:.3f}<br>
            <b>Longitude:</b> {row['longitude']:.3f}
            """

            folium.CircleMarker(

                location=[
                    row["latitude"],
                    row["longitude"]
                ],

                radius=6,

                color=color,

                fill=True,

                fill_color=color,

                fill_opacity=0.8,

                weight=2,

                popup=folium.Popup(
                    popup_text,
                    max_width=250
                ),

                tooltip=(
                    f"Cluster {cluster} | "
                    f"AOD: {row['AOD_mean']:.3f}"
                )

            ).add_to(regional_map)

        # ----------------------------------------------------
        # DISPLAY MAP
        # ----------------------------------------------------

        st_folium(
            regional_map,
            width=1200,
            height=600,
            returned_objects=[]
        )

        st.caption(
            "Each circle represents one regional observation. "
            "Circle colours indicate cluster membership."
        )

    # --------------------------------------------------------
    # STEP 5: CLUSTER DISTRIBUTION
    # --------------------------------------------------------

    st.divider()

    st.subheader("Cluster Distribution in Selected AOD Range")

    cluster_counts = (
        map_df["Cluster_K3"]
        .value_counts()
        .sort_index()
    )

    col1, col2 = st.columns(2)

    with col1:

        st.bar_chart(cluster_counts)

    with col2:

        distribution_table = pd.DataFrame({
            "Cluster": [
                f"Cluster {int(c)}"
                for c in cluster_counts.index
            ],

            "Regional Observations": cluster_counts.values
        })

        st.dataframe(
            distribution_table,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------------
    # STEP 6: COORDINATE PREVIEW
    # --------------------------------------------------------

    with st.expander("View geographical coordinate data"):

        st.dataframe(
            map_df[[
                "latitude",
                "longitude",
                "AOD_mean",
                "LST_mean",
                "Cluster_K3"
            ]],
            use_container_width=True,
            hide_index=True
        )
# ============================================================
# TAB 3: REGIONAL DATA
# ============================================================

with tab3:

    st.subheader("Regional Dataset Explorer")

    st.caption(
        "Explore regional observations and their "
        "environmental characteristics."
    )

    cluster_options = (
        ["All Clusters"] +
        [
            get_cluster_name(c)
            for c in available_clusters
        ]
    )

    selected_cluster = st.selectbox(
        "Select Cluster",
        cluster_options
    )

    table_df = filtered_df.copy()

    if selected_cluster != "All Clusters":

        cluster_number = int(
            selected_cluster.split()[-1]
        )

        table_df = table_df[
            table_df["Cluster_K3"] == cluster_number
        ]

    preferred_columns = [
        "Cluster_K3",
        "AOD_mean",
        "LST_mean",
        "Rainfall_mean",
        "Rainfall_positive_pct",
        "Smoke_count",
        "Fire_count"
    ]

    display_columns = [
        col for col in preferred_columns
        if col in table_df.columns
    ]

    if latitude_col and latitude_col in table_df.columns:

        display_columns.insert(0, latitude_col)

    if longitude_col and longitude_col in table_df.columns:

        display_columns.insert(1, longitude_col)

    st.metric(
        "Matching Regional Observations",
        len(table_df)
    )

    st.dataframe(
        table_df[display_columns],
        use_container_width=True,
        hide_index=True
    )

    csv_data = table_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Dataset",
        data=csv_data,
        file_name="filtered_regional_dataset.csv",
        mime="text/csv"
    )


# ============================================================
# TAB 4: METHODOLOGY
# ============================================================

with tab4:

    st.header("Project Methodology")

    st.caption(
        "Workflow used to generate regional environmental profiles."
    )

    with st.expander("1. Satellite Data Source"):

        st.write("""
        The project uses environmental data derived
        from INSAT-3D satellite observations.

        MOSDAC stands for Meteorological and Oceanographic
        Satellite Data Archival Centre.
        """)

    with st.expander("2. Regional Preparation"):

        st.write("""
        Satellite-derived observations were prepared
        into a regional dataset containing
        430 regional observations.
        """)

    with st.expander("3. Feature Selection"):

        st.write("""
        Two features were selected for the current
        clustering experiment:

        - AOD_mean: Mean Aerosol Optical Depth.
        - LST_mean: Mean Land Surface Temperature.

        Other environmental variables are available
        in the dataset but were not used as inputs
        for the current K-Means experiment.
        """)

    with st.expander("4. Feature Scaling"):

        st.write("""
        Feature scaling was applied before clustering
        so that differences in numerical scales
        would not dominate the distance calculations.
        """)

    with st.expander("5. K-Means Clustering"):

        st.write("""
        K-Means clustering was used to group regional
        observations based on AOD and LST characteristics.

        The current working solution uses three clusters (K=3).
        """)

    with st.expander("6. Model Evaluation"):

        st.write("""
        The experiments were evaluated using:

        - WCSS
        - Silhouette Score
        - Davies-Bouldin Index
        - Adjusted Rand Index

        These measures assess cluster compactness,
        separation and consistency.
        """)

    with st.expander("7. Scientific Interpretation"):

        st.write("""
        The clusters represent different regional
        environmental profiles.

        AOD indicates aerosol loading in the atmospheric
        column. It is not a direct measurement of
        ground-level PM2.5 or AQI.

        LST represents land surface temperature,
        not air temperature.

        The current analysis uses one observation period.
        It does not establish persistent pollution hotspots.
        """)

    st.divider()

    st.subheader("Important Project Limitations")

    st.warning("""
    1. Current analysis uses one observation period.

    2. AOD is not equivalent to ground-level PM2.5.

    3. LST is not equivalent to air temperature.

    4. Clusters represent environmental similarity,
       not confirmed pollution sources.

    5. Multi-date analysis and ground-based validation
       are needed to establish persistent hotspots.
    """)


# ============================================================
# 13. FOOTER
# ============================================================

st.divider()

st.markdown(
    "### 🌍 Regional Pollution Hotspot Profiling"
)

st.caption(
    "INSAT-3D Satellite Data | MOSDAC | K-Means Clustering"
)

st.caption(
    "Regional Environmental Analysis | 18 June 2024"
)