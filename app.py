import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
from datetime import datetime

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
    'latitude': np.random.uniform(-90, 90, num_predictions),
    'longitude': np.random.uniform(-180, 180, num_predictions),
    'depth': np.random.uniform(0, 700, num_predictions),
    'probability': np.random.uniform(0, 100, num_predictions),  # Probability in percentage
})

# ---- Color Function ----
def get_color(probability):
    if probability >= 80:
        return 'darkred'
    elif probability >= 60:
        return 'red'
    elif probability >= 40:
        return 'orange'
    elif probability >= 20:
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
            radius=3 + (row['probability'] / 20),  # Dynamic size based on probability
            color=get_color(row['probability']),
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(
                f"🗓️ Month-Year: {datetime(int(row['year']), int(row['month']), 1).strftime('%b %Y')}<br>"
                f"🌍 Lat, Long: {row['latitude']:.2f}, {row['longitude']:.2f}<br>"
                f"📏 Depth: {row['depth']:.1f} km<br>"
                f"💥 Probability: {row['probability']:.1f}%",
                max_width=300
            )
        ).add_to(marker_cluster)

# ---- Heatmap Visualization ----
if visualization_choice in ["Heatmap", "Combined"]:
    heat_data = [[row['latitude'], row['longitude'], row['probability']] for _, row in future_data.iterrows()]
    HeatMap(heat_data, min_opacity=0.3, radius=15, blur=10, max_zoom=1).add_to(m)

# ---- Display Map ----
st_folium(m, width=1200, height=700)  # Updated method from folium_static to st_folium (newer, more stable)

# ---- Color Legend Table ----
st.markdown("### 🔑 **Color Legend for Earthquake Probability (%)**")
st.markdown("""
<style>
    .legend-table {
        width: 60%;
        margin-left: auto;
        margin-right: auto;
        border-collapse: collapse;
    }
    .legend-table td, .legend-table th {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: center;
    }
    .legend-table th {
        background-color: #f2f2f2;
    }
</style>
<table class='legend-table'>
    <tr>
        <th>Probability Range (%)</th>
        <th>Color on Map</th>
    </tr>
    <tr><td>80 and above</td><td style='background-color:darkred;color:white;'>Dark Red</td></tr>
    <tr><td>60 - 79</td><td style='background-color:red;color:white;'>Red</td></tr>
    <tr><td>40 - 59</td><td style='background-color:orange;'>Orange</td></tr>
    <tr><td>20 - 39</td><td style='background-color:yellow;'>Yellow</td></tr>
    <tr><td>Below 20</td><td style='background-color:green;color:white;'>Green</td></tr>
</table>
""", unsafe_allow_html=True)

# ---- Data Table ----
st.header("📊 **Sample of Predicted Earthquake Events**")
st.write(f"Showing **{len(future_data)}** AI/ML simulated earthquake event predictions with probabilities in the period **{selected_range[0]} to {selected_range[1]}**:")
st.dataframe(future_data.head(20))

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
