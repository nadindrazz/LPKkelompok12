import streamlit as st
import pandas as pd
import random
from datetime import datetime

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Lab Environment Monitoring System",
    page_icon="🌡️",
    layout="wide"
)

# ==========================================
# JUDUL
# ==========================================

st.title("🌡️ Lab Environment Monitoring System")

st.write(
    "Aplikasi monitoring suhu, kelembapan, dan tekanan laboratorium."
)

st.divider()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("⚙️ Pengaturan Monitoring")

max_data = st.sidebar.slider(
    "Jumlah Data Grafik",
    min_value=5,
    max_value=30,
    value=10
)

# ==========================================
# SESSION STATE
# ==========================================

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Waktu", "Suhu", "Kelembapan", "Tekanan"]
    )

# ==========================================
# BUTTON REFRESH
# ==========================================

if st.button("🔄 Refresh Data"):

    suhu = random.randint(22, 35)
    kelembapan = random.randint(40, 90)
    tekanan = random.randint(990, 1020)

    waktu = datetime.now().strftime("%H:%M:%S")

    new_data = pd.DataFrame({
        "Waktu": [waktu],
        "Suhu": [suhu],
        "Kelembapan": [kelembapan],
        "Tekanan": [tekanan]
    })

    st.session_state.data = pd.concat(
        [st.session_state.data, new_data],
        ignore_index=True
    )

    st.session_state.data = st.session_state.data.tail(max_data)

# ==========================================
# TAMPILAN DATA TERAKHIR
# ==========================================

if not st.session_state.data.empty:

    latest = st.session_state.data.iloc[-1]

    suhu = latest["Suhu"]
    kelembapan = latest["Kelembapan"]
    tekanan = latest["Tekanan"]

else:

    suhu = 0
    kelembapan = 0
    tekanan = 0

# ==========================================
# DASHBOARD
# ==========================================

st.subheader("📊 Dashboard Monitoring")

col1, col2, col3 = st.columns(3)

col1.metric("🌡️ Suhu", f"{suhu} °C")
col2.metric("💧 Kelembapan", f"{kelembapan} %")
col3.metric("🌪️ Tekanan", f"{tekanan} hPa")

st.divider()

# ==========================================
# STATUS LAB
# ==========================================

st.subheader("🚨 Status Laboratorium")

if suhu > 30:
    st.error("⚠️ Suhu laboratorium terlalu tinggi!")

elif suhu < 24:
    st.warning("⚠️ Suhu laboratorium terlalu rendah!")

else:
    st.success("✅ Suhu laboratorium normal")

if kelembapan > 80:
    st.warning("⚠️ Kelembapan terlalu tinggi!")

elif kelembapan < 45:
    st.warning("⚠️ Kelembapan terlalu rendah!")

else:
    st.success("✅ Kelembapan normal")

st.divider()

# ==========================================
# GRAFIK
# ==========================================

st.subheader("📈 Grafik Monitoring")

if not st.session_state.data.empty:

    chart_data = st.session_state.data.set_index("Waktu")

    st.line_chart(chart_data)

st.divider()

# ==========================================
# TABEL DATA
# ==========================================

st.subheader("📋 Data Monitoring")

st.dataframe(
    st.session_state.data,
    use_container_width=True
)

st.divider()

# ==========================================
# DOWNLOAD CSV
# ==========================================

csv = st.session_state.data.to_csv(index=False)

st.download_button(
    label="⬇️ Download Data CSV",
    data=csv,
    file_name="lab_monitoring_data.csv",
    mime="text/csv"
)
