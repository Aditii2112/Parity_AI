import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Parity AI", page_icon="%", layout="wide")

# Sidebar for status
with st.sidebar:
    st.title("System Status")
    st.success("Connected to MCP Core")
    st.info(f"Last Sync: {datetime.now().strftime('%H:%M:%S')}")
    st.divider()
    st.markdown("🔍 **Active Scopes:**\n* Gmail Search\n* Slack Search\n* Conflict Logic")

st.title("Parity AI")
st.caption("Autonomous Cross-Platform Data Auditor")

user_query = st.text_input("Query", placeholder="e.g., Check Suyash's latest updates for contradictions...")

if st.button("Analyze Pipeline"):
    if user_query:
        # Visual feedback for the "Agentic" process
        status_cols = st.columns(3)
        with status_cols[0]: st.write("Fetching Gmail...")
        with status_cols[1]: st.write("Scanning Slack...")
        with status_cols[2]: st.write("Auditing Context...")
        
        with st.spinner("Processing..."):
            try:
                response = requests.post("http://localhost:8000/ask", json={"text": user_query})
                if response.status_code == 200:
                    answer = response.json().get("answer")
                    
                    # 🚩 CONTRADICTION CHECK
                    # We look for keywords the agent uses when it finds a mismatch
                    is_conflict = any(word in answer.upper() for word in ["CONTRADICTION", "STATUS CHANGE", "MISMATCH", "CONFLICT"])
                    
                    st.divider()
                    
                    if is_conflict:
                        st.error("⚠️ CRITICAL CONTRADICTION DETECTED")
                    else:
                        st.success("PLATFORM DATA ALIGNED")

                    with st.container(border=True):
                        st.markdown(answer)
                        
                else:
                    st.error("Backend returned an error. Check terminal.")
            except Exception as e:
                st.error(f"Connection Failed: {e}")