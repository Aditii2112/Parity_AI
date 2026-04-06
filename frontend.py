import streamlit as st
import requests

st.set_page_config(page_title="Intelligence Hub", page_icon="📊")

st.title("Cross-Platform Intelligence")
st.markdown("Query your Slack and Gmail data using autonomous AI agents.")

# User Input
user_query = st.text_input("What would you like to check?", 
                          placeholder="e.g., Check for contradictions between Aditi's emails and Slack.")

if st.button("Analyze"):
    if user_query:
        with st.spinner(" Agent is navigating platforms..."):
            try:
                response = requests.post("http://localhost:8000/ask", json={"text": user_query})
                if response.status_code == 200:
                    answer = response.json().get("answer")
                    
                    st.divider()
                    st.subheader("🤖 Agent Analysis")
                    # Using a container with a border for a professional look
                    with st.container(border=True):
                        st.write(answer)
                else:
                    st.error("The agent encountered an error processing the request.")
            except Exception as e:
                st.error(f"Backend Connection Failed: {e}")
    else:
        st.warning("Please enter a query.")

st.sidebar.info("Connected to: Slack MCP & Gmail MCP")