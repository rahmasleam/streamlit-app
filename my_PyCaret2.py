import pandas as pd
import streamlit as st
import os 

# Import profiling capability
# import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

# ML stuff
# from pycaret.regression import setup, compare_models, pull, save_model, load_model
from pycaret.regression import *

from operator import index
import plotly.express as px


with st.sidebar:
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
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
    # st.title("Exploratory Data Analysis")
    # profile_df = df.profile_report()
    # st_profile_report(profile_df)
    pass

if choice == 'Modeling':
    # chosen_target = st.selectbox('Choose the Target Column', df.columns)
    # if st.button('Run Modelling'): 
    #     setup(df, target=chosen_target, silent=True)
    #     setup_df = pull()
    #     st.dataframe(setup_df)
    #     best_model = compare_models()
    #     compare_df = pull()
    #     st.dataframe(compare_df)
    #     save_model(best_model, 'best_model')

    pass

if choice == "ML":
    st.title("Machine Learning go BRR***")
    target = st.selectbox('Choose the Target Column', df.columns)
    if st.button('Run Modelling'):
        # Setup the machine learning experiment
        setup(df, target=target)
        setup_df = pull()
        st.info("This is the ML Experiment settings")
        st.dataframe(setup_df)

        # Compare and select the best model
        best_model = compare_models()
        compare_df = pull()
        st.info("This is the ML Model")
        st.dataframe(compare_df)
        
        # plot residuals
        st.subheader("Residuals Plot")
        st.plotly_chart(plot_model(best_model, plot = 'residuals'))
        
        # plot error
        st.subheader("Error Plot")
        st.plotly_chart(plot_model(best_model, plot = 'error'))
        
        # plot feature importance
        st.subheader("Feature Importance Plot")
        st.plotly_chart(plot_model(best_model, plot = 'feature'))

        #*****
        # AUC plot
        st.subheader("AUC plot")
        st.plotly_chart(plot_model(best_model, plot = 'auc'))

        # Decision Boundary
        st.subheader("Decision Boundary")
        st.plotly_chart(plot_model(best_model, plot = 'boundary'))

        # Precision Recall Curve
        st.subheader("Precision Recall Curv")
        st.plotly_chart(plot_model(best_model, plot = 'pr'))

        # Validation Curve
        st.subheader("Validation Curve")
        st.plotly_chart(plot_model(best_model, plot = 'vc'))
        
        # Evaluate Model
        st.subheader("Evaluate Model")
        st.plotly_char(evaluate_model(best_model))
        
#         # predict on test set
#         holdout_pred = predict_model(best_model)
        
#         # show predictions 
#         st.subheader("Predictions on Test Set")
#         st.dataframe(holdout_pred.head())
        
#         # Display the best model
#         st.subheader("Best Model")
#         st.write(best_model)

#         best_model

if choice == "ML" and df is not None:
    st.title("Machine Learning go BRR***")
    target = st.selectbox('Choose the Target Column', df.columns)
    
    if st.button('Run Modelling'):
        # Verify that the target variable is set correctly
        if target not in df.columns:
            st.error("Invalid target variable selected.")
        else:
            # Setup the machine learning experiment
            ml_setup = setup(df, target=target)
            setup_df = pull()
            st.info("This is the ML Experiment settings")
            st.dataframe(setup_df)
            
            # Check if the setup successfully loaded data
            if not setup_df.empty:
                # Compare and select the best model
                best_model = compare_models(exclude=['lr', 'knn', 'nb', 'dt', 'svm', 'rbfsvm', 'gpc', 'mlp', 'ridge', 'rf', 'qda', 'ada', 'xgboost', 'lightgbm', 'catboost'])
                compare_df = pull()
                st.info("This is the ML Model")
                st.dataframe(compare_df)
                
                # Plot residuals, error, and feature importance
                st.subheader("Residuals Plot")
                st.plotly_chart(plot_model(best_model, plot='residuals'))
                st.subheader("Error Plot")
                st.plotly_chart(plot_model(best_model, plot='error'))
                st.subheader("Feature Importance Plot")
                st.plotly_chart(plot_model(best_model, plot='feature'))
                
                # Predict on test set
                holdout_pred = predict_model(best_model)
                
                # Show predictions
                st.subheader("Predictions on Test Set")
                st.dataframe(holdout_pred.head())
                
                # Display the best model
                st.subheader("Best Model")
                st.write(best_model)
            else:
                st.warning("The setup did not load data correctly. Please check your dataset and target variable.")


if choice == "Download": 
    with open('best_model.pkl', 'rb') as f: 
        st.download_button('Download Model', f, file_name="best_model.pkl")


dashboard(best_model,display_format='inline')
check_fairness(best_model)