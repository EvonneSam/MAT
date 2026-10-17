import streamlit as st
import time
import requests
import numpy as np
import pandas as pd

st.set_page_config(page_title="MAT: Flight-Safe AI", layout="wide")

st.title("MAT: AI-Powered Aircraft Engine Health Monitor")
st.caption("Live Enterprise Inference Powered by IBM Z LinuxONE | Architecture Target: s390x")
st.markdown("---")

# 1. Establish Infrastructure Connection (Pointed directly to her active server)
MAINFRAME_IP = "148.100.99.48"  # Her verified server IP address
API_URL = f"http://{MAINFRAME_IP}:5000/predict"

# Layout Columns
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 Live Telemetry Stream")
    temp_metric = st.empty()
    speed_metric = st.empty()
    st.markdown("---")
    st.subheader("🚨 System Directives")
    alert_placeholder = st.empty()

with col2:
    st.subheader("📈 Real-Time Engine Degradation Curve")
    chart_placeholder = st.empty()
    st.subheader("🖥️ Mainframe Infrastructure Transmission Log")
    log_placeholder = st.empty()

# 2. Initialize simulated streaming historical state data arrays
history_data = []
log_history = []

# Baseline normal parameters before decay starts
core_temp = 530.0
fan_speed = 1250.0
cycle_count = 0

# 3. Continuous Tracking Automation Loop
while True:
    cycle_count += 1
    
    # Simulate realistic ascending operational wear and strain signatures
    if cycle_count > 10:
        core_temp += np.random.uniform(0.5, 4.5)
        fan_speed += np.random.uniform(2.0, 15.0)
    else:
        core_temp += np.random.uniform(-0.5, 1.0)
        fan_speed += np.random.uniform(-1.0, 3.0)
        
    # Render updated text metric indicators inside the layout
    temp_metric.metric("Core Temperature (°C)", f"{core_temp:.2f}", delta=f"{core_temp-530.0:.2f}" if cycle_count > 1 else None)
    speed_metric.metric("Turbine Fan Speed (RPM)", f"{int(fan_speed)}", delta=f"{int(fan_speed-1250.0)}" if cycle_count > 1 else None)
    
    # 4. Transmit data payload over the network to the running mainframe API
    try:
        start_time = time.time()
        response = requests.post(API_URL, json={"sensors": [core_temp, fan_speed]}, timeout=2).json()
        network_latency = (time.time() - start_time) * 1000 # Calculate round-trip delay
        
        # Pull response parameters out of the mainframe JSON object
        rul = response.get('remaining_useful_cycles', 0)
        status = response.get('engine_status', 'UNKNOWN')
        action = response.get('recommended_action', 'NONE')
        
        # Append parameters to graph timeline tracking history list
        history_data.append({"Cycle": cycle_count, "Core Temperature": core_temp, "Predicted RUL": rul})
        df_chart = pd.DataFrame(history_data)
        chart_placeholder.line_chart(df_chart.set_index("Cycle")[["Core Temperature", "Predicted RUL"]])
        
        # Push a fresh network timestamp directly into our log console box
        log_line = f"[{time.strftime('%H:%M:%S')}] Ingested cycle {cycle_count:03d} | Payload: [{core_temp:.1f}°C, {int(fan_speed)}RPM] | Mainframe Inference: {response.get('mainframe_inference_latency')} | RTT: {network_latency:.1f}ms"
        log_history.insert(0, log_line)
        log_placeholder.code("\n".join(log_history[:6]), language="bash")
        
        # 5. Dynamic Safety Evaluation Logic
        with alert_placeholder.container():
            st.metric("Predicted Remaining Useful Life", f"{rul} cycles")
            if "CRITICAL" in status:
                st.error(f"🔴 STATUS: {status}")
                st.error(f"👉 ACTION REQUIRED: {action}")
            elif "WARNING" in status:
                st.warning(f"🟡 STATUS: {status}")
                st.warning(f"👉 ACTION REQUIRED: {action}")
            else:
                st.success(f"🟢 STATUS: {status}")
                st.info(f"👉 ACTION REQUIRED: {action}")
                
    except Exception as e:
        with alert_placeholder.container():
            st.error(f"Connection Loss: Unable to reach API server at {MAINFRAME_IP}. Verify your teammate's Docker container status.")
            
    # Interval pace before requesting the next simulated real-time telemetry array packet
    time.sleep(1.0)
