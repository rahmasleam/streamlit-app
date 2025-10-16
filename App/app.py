# importing libraries
import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px
from pandas.api.types import is_numeric_dtype, is_string_dtype

# Initialize session state for df
if 'df' not in st.session_state:
    st.session_state.df = None

with st.sidebar:
    st.image("https://www.onepointltd.com/wp-content/uploads/2019/12/shutterstock_1166533285-Converted-02.png")
    st.title("AutoStreamMl")
    choice = st.radio("Navigation", ["Upload","Pre-processing","Visualization","ML"])

def check_df():
    if st.session_state.df is None:
        st.warning("⚠️ Please upload the data first from the tab 'Upload'!")
        st.stop()

if choice == 'Upload':
    st.markdown('# Analysis data')
    st.header('Upload data: ')
    file_path = st.file_uploader("Upload the data file")

    if file_path is not None:
        if file_path.name[-4:] == '.csv':
            st.session_state.df = pd.read_csv(file_path)
            st.success('Data loaded successfully!')
        elif file_path.name[-5:] == '.xlsx' or file_path.name[-4:] == '.xls':
            st.session_state.df = pd.read_excel(file_path)
            st.success('Data loaded successfully!')
        # Display the data
        st.header('Loaded data: ')
        st.dataframe(st.session_state.df.head(5))

if choice == "Pre-processing":
    check_df()
    df = st.session_state.df.copy()  # Copy to avoid modifying original
    st.markdown('# Analysis data')
    st.header('Data Preprocessing: ')

    # Data types
    type_col = df.dtypes
    st.header('Data type of each column')
    btn1 = st.button('show data type of col')
    if btn1:
        for col, dtype in type_col.items():
            st.write(f'{col}: {dtype}')

    # Data cleaning - Check NA
    st.header('Data Cleaning')
    btn = st.button('show sum NA')
    if btn:
        na_df = df.isna().sum()
        for col, na_count in na_df.items():
            if na_count > 0:
                st.write(f'{col}: {na_count}')
    
    na = df.isnull().any().any()
    if na:
        st.markdown('## Handle missing values')
        option = st.radio("Select To Clean data from NAs", ['Data without Remove NA','Mean (Numeric only)','Median (Numeric only)','Drop NA','Fillna with 0'])
        if option == 'Data without Remove NA':
            st.success("Done")
        elif option == 'Mean (Numeric only)':
            df = df.fillna(df.select_dtypes(include=np.number).mean())
            st.success("Done")
        elif option == 'Median (Numeric only)':
            df = df.fillna(df.select_dtypes(include=np.number).median())
            st.success("Done")
        elif option == 'Drop NA':
            df = df.dropna()
            st.success("Done")
        elif option == 'Fillna with 0':
            df.fillna(0, inplace=True)
            st.success("Done")
    
    # Encode categorical
    st.markdown('## Encode categorical features')
    for col in df.select_dtypes(include='object'):
        df[col] = df[col].astype('category')
    st.success("Done")

    # Drop columns
    st.subheader("Select Columns to Drop ")
    columns_to_drop = st.multiselect("Select columns to drop", df.columns)
    df = df.drop(columns=columns_to_drop)

    # Types
    st.subheader("Types of Column Categorical or Numerical")
    col_types = {}
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            col_types[col] = "Numerical"
        elif is_string_dtype(df[col]):
            col_types[col] = "Categorical"
        else:
            col_types[col] = "Other"
    st.dataframe(col_types, use_container_width=True)
    
    # Save back to session
    st.session_state.df = df

if choice == 'Visualization':
    check_df()
    df = st.session_state.df
    st.header('Data Visualization: ')
    n_col = list(df.columns)

    # Matplotlib
    st.header("Matplotlib")

    st.subheader("Histogram")
    option = st.selectbox("Select Column", n_col)
    fig, ax = plt.subplots(figsize=(15,8))
    sns.histplot(data=df, x=option, ax=ax)
    st.pyplot(fig)

    st.subheader("Distribution Plot")
    option = st.selectbox("Select Column", n_col, key=1)
    fig, ax = plt.subplots(figsize=(15,8))
    sns.histplot(data=df, x=option, kde=True, ax=ax)
    st.pyplot(fig)
    
    st.subheader("Box Plot")
    option = st.selectbox("Select Column", n_col, key=2)
    fig, ax = plt.subplots(figsize=(15,8))
    sns.boxplot(data=df, y=option, ax=ax)
    st.pyplot(fig)
    
    st.subheader("Heatmap")
    fig, ax = plt.subplots(figsize=(15,8))
    sns.heatmap(df.corr(), annot=True, ax=ax)
    st.pyplot(fig)
    
    # Plotly
    st.header("Plotly")

    st.subheader("Scatter Plot")
    option1 = st.selectbox("Select Column1", n_col, key=3)
    option2 = st.selectbox("Select Column2", n_col, key=4)
    fig = px.scatter(data_frame=df, x=option1, y=option2)
    st.plotly_chart(fig)

    st.subheader('Bar Chart')
    option1 = st.selectbox("Select Column1", n_col, key=5)
    option2 = st.selectbox("Select Column2", n_col, key=6)
    fig = px.bar(data_frame=df, x=option1, color=option2)
    st.plotly_chart(fig)

    st.subheader("Histogram")
    option = st.selectbox("Select Column", n_col, key=7)
    fig = px.histogram(df, x=option, color=option)
    st.plotly_chart(fig)

if choice == "ML":
    check_df()
    df = st.session_state.df
    from pycaret.classification import *
    from pycaret.regression import *    
    st.subheader("PyCaret Model Building")
    target_column = st.selectbox("Select the target column", df.columns)
    
    # Run PyCaret to build a classification model and display the report
    # Classification
    btn2 = st.button('Classification')
    if btn2:
        with st.spinner('Models are being built...it will take some time (2-5 minutes)'):
            setup(df, target=target_column, session_id=123, verbose=False)
            clf_setup = pull()
            st.info("This is the ML Experiment settings")
            st.dataframe(clf_setup)

            st.subheader("Best Classification Model")
            clf_best_model = compare_models()
            compare_clf = pull()
            st.info("This is the ML Model")
            st.dataframe(compare_clf)

    # Run PyCaret to build a regression model and display the report    
    # Regression
    btn3 = st.button('Regression')
    if btn3:
        with st.spinner('Models are being built...it will take some time (2-5 minutes)'):
            setup(df, target=target_column, session_id=456, verbose=False)
            reg_setup = pull()
            st.info("This is the ML Experiment settings")
            st.dataframe(reg_setup)
            
            st.subheader("Best Regression Model")
            reg_best_model = compare_models()
            compare_reg = pull()
            st.info("This is the ML Model")
            st.dataframe(compare_reg)