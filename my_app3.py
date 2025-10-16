import streamlit as st
import pandas as pd

st.title("Streamlit Dashboard")
# st.markdown("_Prototype V0.4.1_")

@st.cache_data
def load_data(file):
    data = pd.read_csv(file)
    return data

with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is None:
    st.info("Upload a file through config", icon="ℹ️")
    st.stop()

df = load_data(uploaded_file)

with st.expander("Data Preview"):
    st.dataframe(df)
