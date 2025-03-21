import sys
from pathlib import Path
import streamlit as st
import requests

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.settings import FLASK_PORT

# Initialize session state
if 'principal' not in st.session_state:
    st.session_state.principal = 1500.0
if 'years' not in st.session_state:
    st.session_state.years = 5
if 'apy' not in st.session_state:
    st.session_state.apy = 4.5

def reset_values():
    """Reset values to defaults"""
    st.session_state.principal = 1500.0
    st.session_state.years = 5
    st.session_state.apy = 4.5

st.title("💰 Compound Interest Calculator")
st.markdown(f"Connected to Flask backend on port `{FLASK_PORT}`")

# Input fields
principal = st.number_input(
    "Initial Amount ($)", 
    min_value=0.0,
    step=100.0,
    key='principal'
)

years = st.number_input(
    "Investment Years", 
    min_value=1,
    max_value=100,
    step=1,
    key='years'
)

apy = st.number_input(
    "Annual Yield (%)", 
    min_value=0.0,
    max_value=100.0,
    step=0.5,
    key='apy'
)

# Button columns
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("🧮 Calculate Future Value"):
        try:
            response = requests.post(
                f"http://localhost:{FLASK_PORT}/calculate",
                json={
                    "principal": st.session_state.principal,
                    "years": st.session_state.years,
                    "apy": st.session_state.apy
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                st.success(f"**Future Value:** ${data['result']:,.2f}")
                st.markdown(f"*Calculation:* `{data['formula']}`")
            else:
                st.error(f"Backend error: {response.json().get('error', 'Unknown error')}")
                
        except requests.ConnectionError:
            st.error("Could not connect to backend! Make sure Flask is running.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

with col6:
    if st.button("♻️ Reset Values", on_click=reset_values):
        st.success("Values reset to defaults!")
