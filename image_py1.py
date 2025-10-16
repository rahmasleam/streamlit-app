import pandas as pd
import streamlit as st
import os  

# Import profiling capability
from streamlit_pandas_profiling import st_profile_report

with st.sidebar:
    # st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    # st.image("https://www.onepointltd.com/wp-content/uploads/2019/12/shutterstock_1166533285-Converted-03.png")
    # st.image("https://www.onepointltd.com/wp-content/uploads/2019/12/shutterstock_1166533285-Converted-02.png")
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno1.png")
    st.title("AutoStreamMl")
    choice = st.radio("Navigation", ["Upload","Profiling","ML","Modelling", "Download"])
    st.info("This project application helps you build and explore your data.")


if os.path.exists('./dataset.csv'):
    df = pd.read_csv('dataset.csv', index_col=None)

if choice == 'Upload':
    st.title("Upload Your Dataset")
    file = st.file_uploader("Upload Your Dataset")
    if file: 
        df = pd.read_csv(file, index_col=None)
        # df.to_csv('dataset.csv', index=None)
        st.dataframe(df)

if choice == 'Profiling': 
    st.image("https://www.onepointltd.com/wp-content/uploads/2019/12/shutterstock_1166533285-Converted-02.png")
    st.title("Exploratory Data Analysis")
    profile_df = df.profile_report()
    st_profile_report(profile_df)