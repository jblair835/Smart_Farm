"""Streamlit Smart Farm App"""
import streamlit as st

from agents.tools.smartfarm_brain import SmartFarmBrain

# Initialize SmartFarmBrain
brain = SmartFarmBrain()

st.set_page_config(page_title="SmartFarm Advisor", layout="wide")

st.title("🌾 SmartFarm Real-Time Advisor")
st.write("Ask anything about irrigation, fertilizer, pesticide timing, risks, or weather.")

# Sidebar inputs
st.sidebar.header("Farm Location")
lat = st.sidebar.number_input("Latitude", value=35.0)
lon = st.sidebar.number_input("Longitude", value=-119.0)

st.sidebar.write("SmartFarm will use this location for real-time weather.")

# Main input
prompt = st.text_area(
    "Farmer Question",
    placeholder="Example: I only have enough water for one irrigation this week. My tomatoes are flowering and soil moisture is low. What should I do?",
    height=150
)

if st.button("Get Advisory"):
    if not prompt.strip():
        st.error("Please enter a question.")
    else:
        with st.spinner("Analyzing your farm conditions..."):
            response = brain.ask(prompt, lat=lat, lon=lon)

        st.success("Advisory Ready!")
        st.write(response)
