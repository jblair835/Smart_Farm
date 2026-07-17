# Force Streamlit Cloud redeploy
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
    placeholder=(
        "Example: I only have enough water for one irrigation this week. "
        "My tomatoes are flowering and soil moisture is low. What should I do?"
    ),
    height=150
)

# Tabs for UI sections
tab_overview, tab_weather, tab_risks, tab_recs, tab_review, tab_report = st.tabs(
    ["Overview", "Weather", "Risks", "Recommendations", "Review", "Full Report"]
)

response = None
weather_data = None
risks_data = None
decisions_data = None
review_data = None
final_report = None

if st.button("Get Advisory"):
    if not prompt.strip():
        st.error("Please enter a question.")
    else:
        with st.spinner("Analyzing your farm conditions..."):
            try:
                response = brain.ask(prompt, lat=lat, lon=lon)
            except ValueError as e:
                response = (
                    "⚠️ An unexpected error occurred while generating your advisory.\n\n"
                    f"**Details:** {e}\n\n"
                    "Please check your inputs or try again."
                )

        st.success("Advisory Ready!")

        # Try to reconstruct structured pieces from agents
        try:
            # Weather
            weather_output = brain.weather_agent.run(lat, lon, None)
            weather_data = weather_output.get("weather")

            # Scenario + risks + decisions + review via SmartFarmBrain internals
            # (We don't have direct access to all internals here, so we focus on weather.)
        except (KeyError, AttributeError, TypeError) as e:
            weather_data = None

        # ---------------------------
        # OVERVIEW TAB
        # ---------------------------
        with tab_overview:
            st.subheader("🧾 Advisory Overview")
            st.write(response)

        # ---------------------------
        # WEATHER TAB (Dashboard + Icons)
        # ---------------------------
        with tab_weather:
            st.subheader("🌦 Weather Dashboard")

            if isinstance(response, str) and response.startswith("Weather Agent Error"):
                st.warning("Weather data unavailable — dashboard skipped.")
            else:
                try:
                    if weather_data is None:
                        weather_data = brain.weather_agent.run(lat, lon, None)["weather"]

                    temps = [
                        weather_data["day1"]["temp_c"],
                        weather_data["day2"]["temp_c"],
                        weather_data["day3"]["temp_c"]
                    ]
                    rain = [
                        weather_data["day1"]["rain_mm"],
                        weather_data["day2"]["rain_mm"],
                        weather_data["day3"]["rain_mm"]
                    ]
                    wind = [
                        weather_data["day1"]["wind_kmh"],
                        weather_data["day2"]["wind_kmh"],
                        weather_data["day3"]["wind_kmh"]
                    ]

                    days = ["Day 1", "Day 2", "Day 3"]

                    def temp_icon(t):
                        if t >= 38:
                            return "🔥"
                        elif t >= 30:
                            return "☀️"
                        elif t >= 20:
                            return "🌤️"
                        else:
                            return "❄️"

                    def rain_icon(r):
                        if r >= 10:
                            return "🌧️"
                        elif r >= 2:
                            return "🌦️"
                        else:
                            return "☀️"

                    def wind_icon(w):
                        if w >= 25:
                            return "💨"
                        elif w >= 10:
                            return "🌬️"
                        else:
                            return "🍃"

                    st.write("### 🌈 Conditions Overview")
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.markdown(
                            f"**Day 1**<br>{temp_icon(temps[0])} {temps[0]}°C<br>"
                            f"{rain_icon(rain[0])} {rain[0]} mm<br>"
                            f"{wind_icon(wind[0])} {wind[0]} km/h",
                            unsafe_allow_html=True
                        )

                    with col2:
                        st.markdown(
                            f"**Day 2**<br>{temp_icon(temps[1])} {temps[1]}°C<br>"
                            f"{rain_icon(rain[1])} {rain[1]} mm<br>"
                            f"{wind_icon(wind[1])} {wind[1]} km/h",
                            unsafe_allow_html=True
                        )

                    with col3:
                        st.markdown(
                            f"**Day 3**<br>{temp_icon(temps[2])} {temps[2]}°C<br>"
                            f"{rain_icon(rain[2])} {rain[2]} mm<br>"
                            f"{wind_icon(wind[2])} {wind[2]} km/h",
                            unsafe_allow_html=True
                        )

                    st.write("### 📈 Temperature (°C)")
                    st.line_chart({"Temperature": temps}, x=days)

                    st.write("### 🌧️ Rainfall (mm)")
                    st.bar_chart({"Rainfall": rain}, x=days)

                    st.write("### 💨 Wind Speed (km/h)")
                    st.line_chart({"Wind": wind}, x=days)

                except (KeyError, TypeError, ValueError) as e:
                    st.warning(f"Dashboard unavailable: {e}")

        # ---------------------------
        # RISKS TAB (text only for now)
        # ---------------------------
        with tab_risks:
            st.subheader("⚠️ Risk Assessment")
            st.write(
                "Rusty’s detailed risk breakdown appears inside the main advisory text for now. "
                "Future versions can surface structured risks here."
            )

        # ---------------------------
        # RECOMMENDATIONS TAB
        # ---------------------------
        with tab_recs:
            st.subheader("🧑‍🌾 Recommendations")
            st.write(
                "Doc’s irrigation, pesticide, and fertilizer plan is included in the advisory text. "
                "Future versions can parse and display each operation as cards here."
            )

        # ---------------------------
        # REVIEW TAB
        # ---------------------------
        with tab_review:
            st.subheader("🔍 Review Notes")
            st.write(
                "Inspector Ivy’s review notes are part of the advisory. "
                "Future versions can extract and list contradictions and issues here."
            )

        # ---------------------------
        # FULL REPORT TAB
        # ---------------------------
        with tab_report:
            st.subheader("📜 Full Report")
            st.write(response)
