import streamlit as st
import pandas as pd
import numpy as np

# --- 1. PAGE CONFIGURATION & ESTHETICS ---
st.set_page_config(
    page_title="Corporate Net Zero Strategy Simulator",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to mimic a clean corporate dashboard layout
st.markdown("""
    <style>
    .metric-container {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #1b365d;
        margin-bottom: 10px;
    }
    .stCheckbox {
        padding: 5px 0px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. MOCK DATA ENGINES (FACT & DIMENSION TABLES) ---
@st.cache_data
def load_emissions_data():
    # Base Operational Footprint Data
    return pd.DataFrame([
        {"Record ID": "EM-001", "Scope": "Scope 1", "Activity": "Manufacturing Plant", "Source": "Natural Gas", "tCO2e": 1250},
        {"Record ID": "EM-002", "Scope": "Scope 1", "Activity": "Company Fleet Vehicles", "Source": "Diesel Fuel", "tCO2e": 450},
        {"Record ID": "EM-003", "Scope": "Scope 1", "Activity": "On-site Generators", "Source": "Diesel Fuel", "tCO2e": 180},
        {"Record ID": "EM-004", "Scope": "Scope 2", "Activity": "Corporate Headquarters", "Source": "Purchased Electricity", "tCO2e": 380},
        {"Record ID": "EM-005", "Scope": "Scope 2", "Activity": "Regional Distribution Center", "Source": "Purchased Electricity", "tCO2e": 620},
        {"Record ID": "EM-006", "Scope": "Scope 3", "Activity": "Supply Chain Logistics", "Source": "Third-Party Freight", "tCO2e": 940},
        {"Record ID": "EM-007", "Scope": "Scope 3", "Activity": "Business Travel", "Source": "Commercial Flights", "tCO2e": 120},
        {"Record ID": "EM-008", "Scope": "Scope 3", "Activity": "Employee Commuting", "Source": "Personal Vehicles", "tCO2e": 210},
    ])

@st.cache_data
def load_credit_scenarios():
    # Carbon Credit Portfolio Database
    return pd.DataFrame([
        {"Project ID": "CR-001", "Type": "Removal", "Project Name": "Amazon Reforestation", "Category": "Forestry", "Capacity": 800, "Cost_per_t": 15},
        {"Project ID": "CR-002", "Type": "Avoidance", "Project Name": "Texas Wind Farm Initiative", "Category": "Renewable", "Capacity": 600, "Cost_per_t": 8},
        {"Project ID": "CR-003", "Type": "Removal", "Project Name": "Mangrove Restoration Kerala", "Category": "Blue Carbon", "Capacity": 1200, "Cost_per_t": 22},
        {"Project ID": "CR-004", "Type": "Avoidance", "Project Name": "Clean Cookstoves Distribution", "Category": "Community", "Capacity": 500, "Cost_per_t": 11},
        {"Project ID": "CR-005", "Type": "Removal", "Project Name": "Direct Air Capture (DAC) Iowa", "Category": "Technology", "Capacity": 1050, "Cost_per_t": 65},
    ])

df_emissions_master = load_emissions_data()
df_credits_master = load_credit_scenarios()

# --- 3. SIDEBAR CONTROLS (THE SLICERS) ---
st.sidebar.image("https://img.icons8.com/color/96/environmental-protection.png", width=80)
st.sidebar.title("Simulation Control Room")
st.sidebar.markdown("Use these operational and procurement slicers to dynamically balance the footprint matrix.")

# --- SLICER 1: EMISSION REDUCTION CONTROLS ---
st.sidebar.header("1. Operational Reduction Slicers")
st.sidebar.markdown("*Simulate optimization targets per scope layer:*")

reduction_scope1 = st.sidebar.slider("Scope 1 Mitigation Target (%)", min_value=0, max_value=100, value=0, step=5)
reduction_scope2 = st.sidebar.slider("Scope 2 Mitigation Target (%)", min_value=0, max_value=100, value=0, step=5)
reduction_scope3 = st.sidebar.slider("Scope 3 Mitigation Target (%)", min_value=0, max_value=100, value=0, step=5)

# --- SLICER 2: CARBON CREDIT PROCUREMENT CONTROLS ---
st.sidebar.markdown("---")
st.sidebar.header("2. Carbon Credit Slicers")
st.sidebar.markdown("*Procure available capacity from certified carbon reserves:*")

selected_projects = []
for index, row in df_credits_master.iterrows():
    # Dynamic label showing cost efficiency and absolute capacity limit
    label = f"{row['Project Name']} ({row['Type']}) [Max: {row['Capacity']} tCO2e @ ${row['Cost_per_t']}/t]"
    is_active = st.sidebar.checkbox(label, value=False, key=row['Project ID'])
    
    if is_active:
        # If toggled, give user a secondary dynamic slider to determine exactly how much capacity to purchase
        purchase_qty = st.sidebar.slider(
            f"Volume to procure from {row['Project Name']}", 
            min_value=0, 
            max_value=int(row['Capacity']), 
            value=int(row['Capacity']),
            step=50,
            key=f"vol_{row['Project ID']}"
        )
        selected_projects.append({
            "Project ID": row['Project ID'],
            "Project Name": row['Project Name'],
            "Type": row['Type'],
            "Procured_tCO2e": purchase_qty,
            "Total_Cost": purchase_qty * row['Cost_per_t']
        })

# --- 4. DATA PROCESSING CORE ---
# Apply Operational Mitigation Reductions dynamically
df_emissions = df_emissions_master.copy()
def apply_reduction(row):
    if row['Scope'] == 'Scope 1': return row['tCO2e'] * (1 - reduction_scope1/100)
    if row['Scope'] == 'Scope 2': return row['tCO2e'] * (1 - reduction_scope2/100)
    if row['Scope'] == 'Scope 3': return row['tCO2e'] * (1 - reduction_scope3/100)
    return row['tCO2e']

df_emissions['Mitigated_tCO2e'] = df_emissions.apply(apply_reduction, axis=1)

# Summarize Totals
gross_baseline = df_emissions['tCO2e'].sum()
current_gross_emissions = df_emissions['Mitigated_tCO2e'].sum()
total_mitigated = gross_baseline - current_gross_emissions

# Process Carbon Offset Procurement
df_procured_credits = pd.DataFrame(selected_projects)
total_offset_capacity = df_procured_credits['Procured_tCO2e'].sum() if not df_procured_credits.empty else 0
total_investment_cost = df_procured_credits['Total_Cost'].sum() if not df_procured_credits.empty else 0

net_footprint = current_gross_emissions - total_offset_capacity

# --- 5. MAIN DASHBOARD DISPLAY LAYER ---
st.title("🌿 GHG Protocol Net Zero Simulation Cockpit")
st.markdown("This modeling matrix tracks real-time carbon data integration against global sustainability disclosure frameworks.")

# --- KPI METRICS ROW ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric(label="Gross Footprint (Post-Mitigation)", value=f"{current_gross_emissions:,.0f} tCO2e", delta=f"-{total_mitigated:,.0f} tCO2e")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric(label="Total Procured Offsets", value=f"{total_offset_capacity:,.0f} tCO2e", delta=f"${total_investment_cost:,.0f} Total CapEx", delta_color="inverse")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    # Highlight Net Zero state
    if net_footprint <= 0:
        st.metric(label="Net Footprint Status", value="0 tCO2e", delta="NET ZERO ACHIEVED! 🎉", delta_color="normal")
    else:
        st.metric(label="Net Footprint Status", value=f"{net_footprint:,.0f} tCO2e", delta=f"+{net_footprint:,.0f} tCO2e Exposure", delta_color="inverse")
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    efficiency = (total_offset_capacity / current_gross_emissions * 100) if current_gross_emissions > 0 else 100
    st.metric(label="Offset Mitigation Coverage", value=f"{min(efficiency, 100):.1f}%")
    st.markdown("</div>", unsafe_allow_html=True)

# --- COMPLIANCE ALERTS ---
if net_footprint <= 0:
    st.success(f"🟩 **Audit Verification Pass:** Net-Zero threshold satisfied. Excess offsets available: {abs(net_footprint):,.0f} tCO2e.")
else:
    progress_val = min(float(total_offset_capacity / current_gross_emissions), 1.0) if current_gross_emissions > 0 else 0.0
    st.error(f"🟥 **Compliance Warning:** Residual carbon exposure detected. Adjust your operational mitigation sliders or secure more offsets.")
    st.progress(progress_val, text=f"Progress toward Net Zero Strategy: {progress_val*100:.1f}%")

st.markdown("---")

# --- DATA VISUALIZATION WINDOWS ---
tab1, tab2 = st.columns([3, 2])

with tab1:
    st.subheader("1. Corporate Carbon Ledger Breakdown")
    # Present operational updates dynamically side by side
    display_df = df_emissions[['Scope', 'Activity', 'Source', 'tCO2e', 'Mitigated_tCO2e']].copy()
    display_df.columns = ['GHG Layer', 'Operational Asset', 'Fuel/Source Asset', 'Baseline (tCO2e)', 'Simulated Output (tCO2e)']
    st.dataframe(display_df.style.format({'Baseline (tCO2e)': '{:,.0f}', 'Simulated Output (tCO2e)': '{:,.0f}'}), use_container_width=True)

with tab2:
    st.subheader("2. Active Credit Procurement Receipts")
    if not df_procured_credits.empty:
        receipt_df = df_procured_credits[['Project Name', 'Type', 'Procured_tCO2e', 'Total_Cost']].copy()
        receipt_df.columns = ['Procured Reserve', 'Credit Type', 'Offset Volume (tCO2e)', 'Investment CapEx']
        st.dataframe(receipt_df.style.format({'Offset Volume (tCO2e)': '{:,.0f}', 'Investment CapEx': '${:,.0f}'}), use_container_width=True)
    else:
        st.info("No external carbon offsets currently selected in procurement slicers.")

# --- FOOTER LOGIC BAR ---
st.markdown("---")
st.caption("🔒 Architecture Engine: Structured Data Schema compliant with Corporate Value Chain Accounting Standards (GHG Protocol Scope 3).")