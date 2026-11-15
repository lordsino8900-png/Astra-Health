"""
ASTRA HEALTH — Advanced Space Medical Suite (Main App)
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from database import init_db, get_crew_list, log_telemetry, get_telemetry_history, save_mental_log, get_mental_logs
from engine import generate_telemetry, get_nasa_hrp_risks, run_autonomous_ai_triage
from visuals import render_3d_anatomical_body, render_telemetry_timeseries
from config import PLANET_ENV

# Initialize database
init_db()

st.set_page_config(
    page_title="ASTRA HEALTH — Deep-Space Medical Suite",
    page_icon="🚀",
    layout="wide"
)

# Custom NASA Mission Control Cyberpunk Styling
st.markdown("""
    <style>
    .stApp { background-color: #080b12; color: #e6edf3; }
    .stSidebar { background-color: #0d1117; }
    </style>
""", unsafe_allow_html=True)

# Sidebar Control Center
st.sidebar.title("🚀 ASTRA CONTROL")
selected_planet = st.sidebar.selectbox("Mission Environment", list(PLANET_ENV.keys()), index=3)

crew_df = get_crew_list()
selected_crew_name = st.sidebar.selectbox("Crew Member", crew_df['name'].tolist())
crew_member = crew_df[crew_df['name'] == selected_crew_name].iloc[0]
crew_id = crew_member['id']

st.sidebar.divider()
solar_flare_active = st.sidebar.toggle("⚡ SIMULATE SOLAR FLARE (SPE)", value=False)

st.sidebar.divider()
menu = st.sidebar.radio("Navigation Modules:", [
    "🛰️ Mission Control & 5 Hazards",
    "🩺 3D Anatomy & SANS Diagnostics",
    "📈 Time-Series Health Analytics",
    "🧠 Behavioral Health & Isolation",
    "☢️ CANS Neutron Radiation Monitor",
    "🤖 Autonomous AI Triage & Protocols"
])

# Generate and store current telemetry tick
telemetry = generate_telemetry(crew_id, selected_planet, solar_flare_active)
log_telemetry(telemetry)

# Header
st.title("ASTRA HEALTH: Autonomous Deep-Space Medical System")
if solar_flare_active:
    st.error("🚨 CRITICAL ALERT: Solar Particle Event active! Neutron and proton flux spike detected across habitat modules.")

if menu == "🛰️ Mission Control & 5 Hazards":
    st.subheader("NASA Human Research Program (HRP) — 5 Hazards of Spaceflight")
    
    col1, col2, col3, col4 = st.columns(4)
    env = PLANET_ENV[selected_planet]
    col1.metric("Gravitational Field", f"{env['gravity']} G")
    col2.metric("Comms Delay", f"{env['delay_min']} min", "Autonomous Mode" if env['delay_min'] > 0 else "Direct Link")
    col3.metric("Radiation Rate", f"{env['radiation_rate']} mSv/day", "CANS Active")
    col4.metric("Confinement Risk", "High", "Crew Behavioral Watch")

    st.divider()
    st.markdown("### Specific Physiological Risk Assessment:")
    risks = get_nasa_hrp_risks(selected_planet, solar_flare_active)
    for r in risks:
        if r["status"] == "CRITICAL EMERGENCY":
            st.error(f"**{r['system']}** [{r['status']}]: {r['desc']}")
        elif r["status"] == "Warning":
            st.warning(f"**{r['system']}** [{r['status']}]: {r['desc']}")
        else:
            st.success(f"**{r['system']}** [{r['status']}]: {r['desc']}")

elif menu == "🩺 3D Anatomy & SANS Diagnostics":
    st.subheader(f"Interactive Anatomical Mapping: {selected_crew_name} ({crew_member['role']})")
    st.markdown("Examine specific deep-space physiological pathologies including SANS, fluid shifts, and skeletal degradation:")
    
    selected_zone = st.selectbox("Anatomical System:", [
        "All Systems", 
        "Ocular & Brain (SANS)", 
        "Cardiovascular System", 
        "Immune / Bone Marrow", 
        "Spine & Bone Density"
    ])
    
    col_left, col_right = st.columns([1, 1])
    with col_left:
        fig_body = render_3d_anatomical_body(selected_zone, solar_flare_active)
        st.plotly_chart(fig_body, use_container_width=True)
        
    with col_right:
        st.markdown("### Medical Protocol & Astronaut Guidance:")
        if selected_zone == "Ocular & Brain (SANS)":
            st.info("**SANS (Spaceflight-Associated Neuro-ocular Syndrome):** Monitor visual acuity with onboard ophthalmoscope. If visual blurring occurs, apply thigh cuffs (lower body negative pressure) to redistribute cephalic fluids.")
        elif selected_zone == "Spine & Bone Density":
            st.info("**Bone Mineral Loss:** Low gravity accelerates calcium leaching. Complete the mandatory 2-hour daily resistance training protocol on the ARED machine.")
        elif selected_zone == "Immune / Bone Marrow":
            st.info("**Immune Biomarkers:** Provide periodic saliva/blood samples to screen for latent herpesvirus reactivation and elevated cortisol levels.")
        else:
            st.success("All anatomical systems operating within acceptable deep-space adaptation boundaries.")

elif menu == "📈 Time-Series Health Analytics":
    st.subheader(f"Dynamic Telemetry Analytics: {selected_crew_name}")
    history_df = get_telemetry_history(crew_id)
    if not history_df.empty:
        fig_trend = render_telemetry_timeseries(history_df)
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown("### Raw Telemetry Stream Log")
        st.dataframe(history_df, use_container_width=True)
    else:
        st.warning("Accumulating telemetry data stream...")

elif menu == "🧠 Behavioral Health & Isolation":
    st.subheader("Psychological Status & Circadian Rhythm Monitoring")
    st.markdown("Long-duration isolation and communication delays require daily self-reporting to prevent behavioral drift.")
    
    with st.form("mental_form"):
        mood = st.slider("Psychological Comfort Score (1 - Critical, 10 - Excellent)", 1, 10, 8)
        sleep = st.number_input("Sleep Duration (Previous 24h in hours)", 0.0, 16.0, 7.5)
        fatigue = st.slider("Fatigue Index (0-100)", 0, 100, 20)
        notes = st.text_area("Subjective symptoms / isolation notes")
        
        submitted = st.form_submit_button("Transmit Log to Ship Computer")
        if submitted:
            save_mental_log(crew_id, mood, sleep, fatigue, notes)
            st.success("Psychological telemetry successfully recorded!")

    mental_df = get_mental_logs(crew_id)
    if not mental_df.empty:
        st.dataframe(mental_df, use_container_width=True)

elif menu == "☢️ CANS Neutron Radiation Monitor":
    st.subheader("Compact Active Neutron Spectrometer (CANS Technology)")
    st.markdown("> *The CANS instrument measures high-energy neutron radiation (~30% of space background), protecting crew from severe biological tissue damage.*")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Tick Dose", f"{telemetry['total_radiation']} mSv")
    c2.metric("Neutron Component (CANS)", f"{telemetry['neutron_dose']} mSv", "High Biological Impact")
    c3.metric("Gamma Component", f"{telemetry['gamma_dose']} mSv")
    
    total_mission = round(telemetry['total_radiation'] * 12.0, 2)
    st.progress(min(total_mission / 500.0, 1.0), text=f"Mission Radiation Limit Used: {total_mission} / 500 mSv")
    
    if solar_flare_active:
        st.error("⚠️ CANS SPE ALERT: High-energy neutron flux spike detected! Take immediate shelter in shielded quarters.")
    else:
        st.success("✅ CANS spectrometer confirms nominal deep-space background radiation levels.")

elif menu == "🤖 Autonomous AI Triage & Protocols":
    st.subheader("Autonomous Medical AI Assistant (Deep-Space Triage)")
    st.markdown("With up to 22 minutes of communication delay from Mars, the onboard AI engine evaluates telemetry and executes protocols locally.")
    
    diagnoses, recommendations = run_autonomous_ai_triage(telemetry, selected_planet, solar_flare_active)
    
    st.markdown("### 🔍 Diagnostic Report:")
    for d in diagnoses:
        if "CRITICAL" in d:
            st.error(d)
        elif "Warning" in d:
            st.warning(d)
        else:
            st.success(d)
        
    st.markdown("### 📋 Autonomous Emergency Protocols:")
    for r in recommendations:
        st.warning(f"- {r}")
        
    st.divider()
    st.markdown("### Emergency Checklist for Crew:")
    st.checkbox("1. Verify airlock hermetic seal and cabin pressure", value=False)
    st.checkbox("2. Inspect CO2 scrubbers and O2 generator levels", value=True)
    st.checkbox("3. Confirm blood glucose and biomarker baseline logs", value=True)