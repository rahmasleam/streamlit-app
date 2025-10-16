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
    choice = st.radio("Navigation", ["Upload","Profiling","ML", "Download"])
    st.info("This project application helps you build and explore your data.")

if os.path.exists('./dataset.csv'):
    df = pd.read_csv('dataset.csv', index_col=None)

if choice == "Upload":
    st.title("Upload Your Dataset")
    file = st.file_uploader("Upload Your Dataset")
    if file:
        df = pd.read_csv(file, index_col=None)
        df.to_csv('dataset.csv', index=None)
        st.dataframe(df)

if choice == "Profiling":
    # st.title("Automated Exploratory Data Analysis")
    # profile_df = df.profile_report()
    # st_profile_report(profile_df)
    pass

if choice == "ML":
    st.image("https://www.onepointltd.com/wp-content/uploads/2019/12/shutterstock_1166533285-Converted-02.png")
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

    # Resultes

    # plot feature importance
    st.write("Feature Importance Plot")
    plot_model(best_model, plot = 'feature',save=True)
    st.image("Feature Importance Plot")
    
    
    # AUC plot
    st.write("AUC plot")
    plot_model(best_model, plot = 'auc',save=True)
    st.image("AUC plot.png")

    # Decision Boundary
    st.write("Decision Boundary")
    plot_model(best_model, plot = 'boundary',save=True)

    # Precision Recall Curve
    st.write("Precision Recall Curv")
    plot_model(best_model, plot = 'pr',save=True)

    # Validation Curve
    st.write("Validation Curve")
    plot_model(best_model, plot = 'vc',save=True)
    
    # # Evaluate Model
    # st.subheader("Evaluate Model")
    # evaluate_model(best_model)
    
    

if choice == "Download":
    pass