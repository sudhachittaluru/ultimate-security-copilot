# ==========================
# 🩵 Ultimate Security Copilot AI (Beautiful UI Edition)
# ==========================

import streamlit as st
from modules.preprocessing import load_and_preprocess
from modules.embeddings import create_index, query_index, model
from modules.anomaly import detect_anomalies
from modules.llm_summary import generate_summary
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
import os

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(page_title="Ultimate Security Copilot AI", page_icon="🛡️", layout="wide")

# ==========================
# CSS
# ==========================
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top left, #0a0a0a, #000);
    color: #e5e7eb;
}
h1, h2, h3 {
    color: #00d4ff !important;
    text-align: center;
    font-weight: 700;
}
.sidebar .sidebar-content {
    background-color: #0f172a;
}
button, .stButton>button {
    background: linear-gradient(90deg, #00d4ff, #0ea5e9);
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #0ea5e9, #00d4ff);
    box-shadow: 0px 0px 15px rgba(0,212,255,0.5);
}
.stat-box {
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# HEADER
# ==========================
st.markdown("<h1>🛡️ Ultimate Security Copilot AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Analyze system logs, detect threats, and get actionable insights in real-time.</p>", unsafe_allow_html=True)
st.markdown("---")

# ==========================
# SIDEBAR SETTINGS
# ==========================
with st.sidebar:
    st.header("⚙️ Settings")
    top_k = st.slider("Top K Logs", 1, 20, 5)
    st.markdown("---")
    st.markdown("🎯 **Customize threat analysis parameters** to fine-tune performance.")

# ==========================
# QUICK STATS
# ==========================
st.subheader("📊 Quick Stats")
colA, colB, colC = st.columns(3)

with colA:
    st.markdown("<div class='stat-box'><h3>1,247</h3><p>Total Logs</p></div>", unsafe_allow_html=True)
with colB:
    st.markdown("<div class='stat-box'><h3>23</h3><p>Threats</p></div>", unsafe_allow_html=True)
with colC:
    st.markdown("<div class='stat-box'><h3>Active</h3><p>Status</p></div>", unsafe_allow_html=True)

st.markdown("---")

# ==========================
# HOW TO USE
# ==========================
st.subheader("⚙️ How to Use")
st.markdown("""
1. 📂 Upload your **system log (.csv)** file  
2. 🧠 Enter a **security query** (e.g., “Show failed logins for user bob”)  
3. 🚀 Click **Analyze Threats** to get real-time insights  
""")

st.markdown("---")

# ==========================
# UPLOAD & QUERY SECTION
# ==========================
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📂 Upload & Analyze")
    uploaded_file = st.file_uploader("Drag and drop your log file here, or click to browse", type=["csv"])
    query = st.text_input("🔍 Enter a Security Query", "Show failed logins for user bob")
    analyze_btn = st.button("🚀 Analyze Threats")

# ==========================
# LOAD & PROCESS LOGS
# ==========================
default_log_path = os.path.join("logs", "system_logs.csv")
file_path = uploaded_file if uploaded_file else default_log_path

try:
    logs = load_and_preprocess(file_path)
    logs = detect_anomalies(logs)
except Exception as e:
    st.error(f"❌ Failed to load logs: {e}")
    st.stop()

# ==========================
# MAIN ANALYSIS
# ==========================
if analyze_btn:
    try:
        index, embeddings = create_index(logs)
        top_logs = query_index(index, model, query or "analyze threats", logs, k=top_k)
        summary = generate_summary(top_logs)

        with col2:
            tabs = st.tabs(["🧠 AI Summary", "📋 Logs", "📈 Charts"])

            with tabs[0]:
                st.markdown(f"""
                <div class='stat-box'>
                    <h3>🧠 AI Threat Summary</h3>
                    <p>{summary}</p>
                </div>
                """, unsafe_allow_html=True)

            with tabs[1]:
                gb = GridOptionsBuilder.from_dataframe(
                    top_logs[['timestamp', 'user', 'ip', 'action', 'status', 'severity']]
                )
                gb.configure_default_column(editable=False, filter=True, sortable=True)
                gridOptions = gb.build()
                AgGrid(top_logs, gridOptions=gridOptions, height=400)

            with tabs[2]:
                fig = px.bar(top_logs, x='user', y='status_num', color='severity',
                             title="🔐 Threat Severity by User")
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Error during analysis: {e}")
else:
    with col2:
        st.info("💡 Upload logs and click **Analyze Threats** to see results.")
