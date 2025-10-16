import streamlit as st
import pandas as pd
import os

# Import profiling capability
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

# ML stuff
from pycaret.regression import *

with st.sidebar:
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno1.png")
    st.title("AutoStreamMl")
    choice = st.radio("Navigation", ["Definition","Upload","Profiling","ML", "Download"])
    

if os.path.exists('./dataset.csv'):
    df = pd.read_csv('dataset.csv', index_col=None)

if choice == 'Definition':
    st.image("https://www.onepointltd.com/wp-content/uploads/2019/12/shutterstock_1166533285-Converted-02.png")
    st.markdown(
        "## ***This web app is a No-Code tool for Exploratory Data Analysis and building Machine Learning model for Regression tasks.***\n"
        "1. Load your dataset file (CSV file):\n"
        "2. Click on *Profile Dataset* button in order to generate the pandas profiling of the dataset:\n"
        "3. Choose your target column:\n"
        "4. Click on *Run Modelling* in order to start the training process.:\n"
        "\n6. Download the Pipline model in your local computer."
    )
    st.info("This project application helps you build and explore your data.")

if choice == "Upload":
    st.image("https://www.onepointltd.com/wp-content/uploads/2019/12/shutterstock_1166533285-Converted-03.png")
    st.title("Upload Your Dataset")
    file = st.file_uploader("Upload Your Dataset")
    if file:
        df = pd.read_csv(file, index_col=None)
        # df.to_csv('dataset.csv', index=None)
        st.dataframe(df)

if choice == "Profiling":
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/dodata1.png")
    st.title("Automated Exploratory Data Analysis")
    profile_df = df.profile_report()
    st_profile_report(profile_df)
    pass

if choice == "ML":
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/dodata3.png")
    st.title("Machine Learning go BRR***")
    from pycaret.datasets import get_data
    data = get_data('diabetes')
    target = st.selectbox('Choose the Target Column', data.columns)
    setup(data=data, target=target, session_id = 123)
    setup_df = pull()
    st.info("This is the ML Experiment settings")
    st.dataframe(setup_df)

    best_model = compare_models()
    compare_df =  pull()
    st.info("This is the ML Model")
    st.dataframe(compare_df)

if choice == "Download": 
    with open('best_model.pkl', 'rb') as f: 
        st.download_button('Download Model', f, file_name="best_model.pkl")