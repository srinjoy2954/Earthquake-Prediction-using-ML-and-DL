import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
from datetime import datetime
import joblib

# ---- Load Trained Model ----
rf_model = joblib.load(r"rf_model_final.pkl")  # Adjust path accordingly

# ---- Streamlit Config ----
st.set_page_config(page_title="Earthquake Prediction Map", layout="wide")
st.title("🌎 Earthquake-Prone Zones AI/ML Prediction Map")
st.markdown("### Predict potential earthquake-prone zones using AI/ML model-based simulated data visualization.")

# ---- Sidebar Controls ----
st.sidebar.header("⚙️ Control Panel")

# Month-Year Selector
st.sidebar.subheader("🕒 **Prediction Time Range**")
today = datetime.today()
future_month_years = [(m, y) for y in range(today.year, today.year + 11) for m in range(1, 13)]
month_year_labels = [f"{datetime(y, m, 1).strftime('%b %Y')}" for m, y in future_month_years]
month_year_dict = {label: (m, y) for label, (m, y) in zip(month_year_labels, future_month_years)}
selected_range = st.sidebar.select_slider("Select Prediction Period", options=month_year_labels, value=(month_year_labels[6], month_year_labels[18]))
start_month, start_year = month_year_dict[selected_range[0]]
end_month, end_year = month_year_dict[selected_range[1]]

# Display Selected Range
st.sidebar.markdown(f"### 🔍 Predicting between **{selected_range[0]}** and **{selected_range[1]}**")

# ---- Map Style Options ----
tile_options = {
    "CartoDB Dark": "CartoDB.DarkMatter",
    "CartoDB Light": "CartoDB.Positron",
    "OpenStreetMap": "OpenStreetMap",
    "Esri Satellite": "Esri.WorldImagery",
}
map_style_choice = st.sidebar.selectbox("🗺️ Map Style", list(tile_options.keys()))
map_type = tile_options[map_style_choice]

# ---- Visualization Type ----
visualization_choice = st.sidebar.radio(
    "📊 Visualization Type",
    ["Markers", "Heatmap", "Combined"],
    index=2
)

# ---- Simulated Data Generation ----
selected_month_years = [(m, y) for (m, y) in future_month_years if (y > start_year or (y == start_year and m >= start_month)) and (y < end_year or (y == end_year and m <= end_month))]
num_predictions = min(500, len(selected_month_years) * 25)  # Dynamic adjustment based on range

np.random.seed(42)  # Reproducibility
future_data = pd.DataFrame({
    'year': np.random.choice([y for (m, y) in selected_month_years], num_predictions),
    'month': np.random.choice([m for (m, y) in selected_month_years], num_predictions),
    'day': np.random.randint(1, 29, num_predictions),  # Add day for model compatibility
    'latitude': np.random.uniform(-90, 90, num_predictions),
    'longitude': np.random.uniform(-180, 180, num_predictions),
    'depth': np.random.uniform(0, 700, num_predictions),
    'significance': np.random.uniform(0, 1000, num_predictions),  # Assumed significance feature
})

# ---- Magnitude Prediction ----
# Predicting using only the required features
future_data['magnitude'] = rf_model.predict(
    future_data[['year', 'month', 'day', 'latitude', 'longitude', 'depth', 'significance']]
)

# ---- Color Function ----
def get_color(magnitude):
    if magnitude >= 6.5:
        return 'darkred'
    elif magnitude >= 5.5:
        return 'red'
    elif magnitude >= 4.5:
        return 'orange'
    elif magnitude >= 3.5:
        return 'yellow'
    else:
        return 'green'

# ---- Earthquake Map ----
st.header("🌐 Interactive Earthquake Prediction Map")

m = folium.Map(
    location=[20, 0],  # Center of world map
    zoom_start=2,
    tiles=map_type,
    control_scale=True
)

# ---- Marker Visualization ----
if visualization_choice in ["Markers", "Combined"]:
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in future_data.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=3 + (row['magnitude'] * 2),  # Radius based on magnitude
            color=get_color(row['magnitude']),
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(
                f"🗓️ Date: {int(row['day'])}-{int(row['month'])}-{int(row['year'])}<br>"
                f"🌍 Lat, Long: {row['latitude']:.2f}, {row['longitude']:.2f}<br>"
                f"📏 Depth: {row['depth']:.1f} km<br>"
                f"⚡ Magnitude: {row['magnitude']:.2f}",
                max_width=300
            )
        ).add_to(marker_cluster)

# ---- Heatmap Visualization ----
if visualization_choice in ["Heatmap", "Combined"]:
    heat_data = [[row['latitude'], row['longitude'], row['magnitude']] for _, row in future_data.iterrows()]
    HeatMap(heat_data, min_opacity=0.3, radius=15, blur=10, max_zoom=1).add_to(m)

# ---- Display Map ----
st_folium(m, width=1200, height=700)

# ---- Color Legend Table ----
st.markdown("### 🔑 **Color Legend for Earthquake Magnitude**")
st.markdown("""
| Magnitude Range       | Color    |
|----------------------|----------|
| ≥ 6.5                | Dark Red |
| 5.5 - 6.4            | Red      |
| 4.5 - 5.4            | Orange   |
| 3.5 - 4.4            | Yellow   |
| < 3.5               | Green    |
""")

# ---- Show Data (Optional) ----
with st.expander("📊 See Raw Prediction Data"):
    st.dataframe(future_data[['year', 'month', 'day', 'latitude', 'longitude', 'depth', 'significance', 'magnitude']])

# ---- Footer & Disclaimer ----
st.markdown("---")
st.markdown("""
## 📢 **Disclaimer & AI/ML Model Insights**

⚠️ **Important Notice**: The earthquake predictions and visualizations presented here are **AI/ML-generated estimations based on simulated datasets and historical seismic patterns**. These results are part of an **academic and research-oriented prototype**, designed to showcase how AI/ML models can simulate possible future earthquake-prone zones.

### 🌍 **Our Approach**:
Earthquakes are natural phenomena influenced by complex geophysical processes. Our AI/ML framework primarily considers historical earthquake data, plate boundary behaviors, and seismic trends to simulate probable events.

### ✅ **Please Note**:
- This platform **does not guarantee real-time earthquake forecasts**.
- Predictions are **statistical estimations**, including small-magnitude frequent events.
- Real occurrences may vary due to unpredictable natural factors.

### 💡 **Key Features Demonstrated**:
- Dynamic **time range selection** for future predictions.
- **Interactive global map** with probability-based visualizations (Markers & Heatmaps).
- Detailed pop-up insights (Lat, Long, Depth, Probability).
- **Combined visualization modes**.
- **Sample tabular data** for analysis.

🚨 **Disclaimer**: This system is **experimental** and should **not be used for emergency or real-time decisions**. Refer to official agencies like **USGS** and **IMD** for verified alerts.  
**Developed for Educational & Research Purposes.**
""")

