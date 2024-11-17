import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

def fetch_data(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


result = fetch_data('http://localhost:8000/apis/home?crypto=btc')
print(result)

# Set page config
st.set_page_config(layout="wide")

# Add custom CSS for the tooltip
st.markdown("""
    <style>
    .tooltip-container {
        position: relative;
        display: inline-flex;
        align-items: center;
    }
    
    .tooltip-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background-color: #f0f2f6;
        color: #0f1215;
        font-size: 12px;
        font-weight: bold;
        margin-left: 5px;
        cursor: help;
    }
    
    .tooltip-content {
        visibility: hidden;
        position: absolute;
        z-index: 1000;
        background-color: #333;
        color: white;
        text-align: center;
        padding: 5px 10px;
        border-radius: 6px;
        font-size: 14px;
        width: max-content;
        max-width: 200px;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        margin-top: 5px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    /* Arrow for tooltip */
    .tooltip-content::after {
        content: "";
        position: absolute;
        bottom: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: transparent transparent #333 transparent;
    }
    
    .tooltip-container:hover .tooltip-content {
        visibility: visible;
        opacity: 1;
    }
    
    .tooltip-icon:hover {
        background-color: #e1e4e8;
    }
    
    /* Additional styles for better layout */
    .slider-label {
        margin-bottom: 5px;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Function to create tooltip
def add_tooltip(label, tooltip_text):
    return f"""
        <div class="tooltip-container">
            {label}
            <div class="tooltip-icon">?
                <span class="tooltip-content">{tooltip_text}</span>
            </div>
        </div>
    """

# Search bar at the top with tooltip
st.markdown(add_tooltip(
    "Search",
    "Enter keywords to filter the dashboard data"
), unsafe_allow_html=True)
search_query = st.text_input("", placeholder="Enter your search term...")

# Generate sample time series data
dates = pd.date_range(start='2024-01-01', end='2024-11-17', freq='D')
values = np.random.normal(loc=100, scale=15, size=len(dates))
df = pd.DataFrame({
    'Date': dates,
    'Value': values
})

# Full width time series graph with tooltip
st.markdown(add_tooltip(
    "Time Series Overview",
    "Shows the trend of values over time. The graph is interactive and can be zoomed."
), unsafe_allow_html=True)
st.line_chart(
    df.set_index('Date'),
    use_container_width=True,
    height=400
)

# Create two columns for settings
col1, col2 = st.columns(2)

# Settings with sliders in first column
with col1:
    st.markdown(add_tooltip(
        '<div class="slider-label">Quality Score</div>',
        "Measure of overall quality metrics (0-100)"
    ), unsafe_allow_html=True)
    score1 = st.slider("", 0, 100, 50, key="quality")
    
    st.markdown(add_tooltip(
        '<div class="slider-label">Performance Score</div>',
        "System performance rating based on response times"
    ), unsafe_allow_html=True)
    score2 = st.slider("", 0, 100, 75, key="performance")
    
    st.markdown(add_tooltip(
        '<div class="slider-label">Reliability Score</div>',
        "Measure of system uptime and stability"
    ), unsafe_allow_html=True)
    score3 = st.slider("", 0, 100, 60, key="reliability")

# Settings with sliders in second column
with col2:
    st.markdown(add_tooltip(
        '<div class="slider-label">Efficiency Score</div>',
        "Rating of resource utilization and process efficiency"
    ), unsafe_allow_html=True)
    score4 = st.slider("", 0, 100, 80, key="efficiency")
    
    st.markdown(add_tooltip(
        '<div class="slider-label">Overall Score</div>',
        "Composite score combining all metrics"
    ), unsafe_allow_html=True)
    score5 = st.slider("", 0, 100, 70, key="overall")

# Save button with tooltip
st.markdown(add_tooltip(
    "Save Settings",
    "Click to save all current dashboard settings and scores"
), unsafe_allow_html=True)
if st.button("Save Settings", type="primary"):
    st.success("Settings saved successfully!")
    
    settings = {
        "quality_score": score1,
        "performance_score": score2,
        "reliability_score": score3,
        "efficiency_score": score4,
        "overall_score": score5
    }
    st.write("Saved settings:", settings)