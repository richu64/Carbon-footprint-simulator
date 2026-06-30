import streamlit as st

st.title("🌿 GHG Protocol Net Zero Simulator")

# 1. Base Emissions
gross_emissions = 4150
st.metric(label="Total Operational Footprint (Scope 1, 2, 3)", value=f"{gross_emissions} tCO2e")

st.subheader("Toggle Carbon Credit Projects:")

# 2. Interactive Toggles
proj_a = st.checkbox("Include Amazon Reforestation Project (-800 tCO2e)")
proj_b = st.checkbox("Include Texas Wind Farm Initiative (-600 tCO2e)")
proj_c = st.checkbox("Include Mangrove Restoration Kerala (-1200 tCO2e)")
proj_d = st.checkbox("Include Clean Cookstoves Distribution (-500 tCO2e)")
proj_e = st.checkbox("Include Direct Air Capture Iowa (-1050 tCO2e)")

# 3. Calculate dynamic offset totals
total_offsets = 0
if proj_a: total_offsets -= 800
if proj_b: total_offsets -= 600
if proj_c: total_offsets -= 1200
if proj_d: total_offsets -= 500
if proj_e: total_offsets -= 1050

net_footprint = gross_emissions + total_offsets

# 4. Dynamic Visual Alert
st.markdown("---")
if net_footprint > 0:
    st.error(f"⚠️ Net Footprint Status: {net_footprint} tCO2e (Net Positive)")
else:
    st.success(f"🌿 Net Footprint Status: {net_footprint} tCO2e (Net Zero Achieved!)")

