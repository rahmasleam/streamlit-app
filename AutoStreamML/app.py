# importing libraries
import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px
import os
from pandas.api.types import is_numeric_dtype, is_string_dtype

with st.sidebar:
    st.image("https://www.onepointltd.com/wp-content/uploads/2019/12/shutterstock_1166533285-Converted-02.png")
    st.title("AutoStreamMl")
    choice = st.radio("Navigation", ["Upload","Pre-processing","Visualization","ML"])

if os.path.exists('./data.csv'):
    df = pd.read_csv('data.csv', index_col=None)
elif os.path.exists('./data.xlsx'):
    df = pd.read_excel('data.xlsx', index_col=None)

if choice == 'Upload':
    st.markdown('# Analysis data')
    st.header('Upload data: ')
    file_path = st.file_uploader("Upload the data file")

    if file_path is not None:
        if file_path.name[-4:] == '.csv':
            df = pd.read_csv(file_path)
            df.to_csv('data.csv', index=None)
            st.write('Data loaded successfully!')
        elif file_path.name[-5:] == '.xlsx' or file_path.name[-4:] == '.xls':
            df = pd.read_excel(file_path)
            df.to_excel('data.xlsx', index=None)
            st.write('Data loaded successfully!')
        # Display the data
        st.header('Loaded data: ')
        st.dataframe(df.head(5))

if choice == "Pre-processing":
    st.markdown('# Analysis data')
    st.header('Data Preprocessing: ')

    # # Preprocessing for data 
    
    # Identify the data types of each column.
    type_col = df.dtypes
    st.header('Data type of each column')
    
    # # as column
    # st.dataframe(type_col)  

    # Not column 
    btn1 = st.button('show data type of col')
    for col, dtype in type_col.items():
        if btn1:
            st.write(f'{col}: {dtype}')

    # # Data cleaning
    # Check NA
    st.header('Data Cleaning')
    btn = st.button('show sum NA')
    if btn:
        na_df = df.isna().sum()
        for col, dtype in na_df.items():
            st.write(f'{col}: {dtype}')
    # Handle missing values.
    na = df.isnull().any().any()
    if na:
        st.markdown('## Handle missing values')
        option = st.radio("Select To Clean data from NAs", ['Data without Remove NA','Mean','Median','Drop NA','Fillna with 0'])
        if option == 'Data without Remove NA':
            st.success("Done")
        elif option == 'Mean':
            df.fillna(df.mean, inplace=True)
            st.success("Done")
        elif option == 'Median':
            df.fillna(df.median, inplace=True)
            st.success("Done")
        elif option == 'Drop NA':
            df.dropna(inplace=True)
            st.success("Done")
        elif option == 'Fillna with 0':
            df.fillna(0, inplace=True)
            st.success("Done")
    # Encode categorical features.
    st.markdown('## Encode categorical features')
    for col in df.select_dtypes(include='object'):
        df[col] = df[col].astype('category')
    st.success("Done")

    # Ask the user to select columns to drop 
    st.subheader("Select Columns to Drop ")

    # Let the user select columns to drop
    columns_to_drop = st.multiselect("Select columns to drop", df.columns)

    # Remove the selected columns
    df = df.drop(columns=columns_to_drop)

    # Dataframe Categorical or Numerical
    st.subheader("Types of Column Categorical or Numerical")
    col_types = {}
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            col_types[col] = "Numerical"
        elif is_string_dtype(df[col]):
            col_types[col] = "Categorical"
        else:
            col_types[col] = "Other"

    st.dataframe(col_types)

if choice == 'Visualization':
    st.header('Data Visualization: ')
    # Make column names in list
    n_col = list(df)

    # matplotlib
    st.header("Matplotlib")

    st.subheader("Histogram")
    option = st.selectbox("Select Column", n_col)
    fig = plt.figure(figsize=(15,8))
    sns.histplot(df[option])
    st.pyplot(fig)

    st.subheader("Histogram")
    option = st.selectbox("Select Column", n_col, key = 1)
    fig = plt.figure(figsize=(15,8))
    sns.distplot(df[option])
    st.pyplot(fig)
    
    st.subheader("Box Plot")
    option = st.selectbox("Select Column1", n_col)
    fig = plt.figure(figsize=(15,8))
    sns.boxplot(data=df, y=df[option])
    st.pyplot(fig)
    
    st.subheader("Heatmap")
    fig = plt.figure(figsize=(15,8))
    sns.heatmap(df.corr(), annot=True)
    st.pyplot(fig)
    
    st.header("Plotly")

    st.subheader("Scatter Plot")
    option1 = st.selectbox("Select Column1", n_col, key = 2)
    option2 = st.selectbox("Select Column2", n_col, key = 3)
    fig = px.scatter(data_frame=df, x= df[option1], y=df[option2])
    st.plotly_chart(fig)

    st.subheader('Bar Chart')
    option1 = st.selectbox("Select Column1", n_col, key = 4)
    option2 = st.selectbox("Select Column2", n_col, key = 5)
    fig = px.bar(data_frame=df, x=df[option1], color=df[option2])
    st.plotly_chart(fig)

    st.subheader("Histogram")
    option = st.selectbox("Select Column", n_col, key = 6)
    fig = px.histogram(df[option],color=df[option])
    st.plotly_chart(fig)


if choice == "ML":
    from pycaret.classification import *
    # Ask the user to select the target column
    st.subheader("PyCaret Model Building")
    target_column = st.selectbox("Select the target column", df.columns)
    
    # Classification Model
    btn2 = st.button('Classification')

    # Run PyCaret to build a classification model and display the report
    if btn2:
        setup(df, target=target_column)
        clf_setup = pull()
        st.info("This is the ML Experiment settings")
        st.dataframe(clf_setup)

        st.subheader("Best Classification Model")
        clf_best_model = compare_models()
        compare_clf =  pull()
        st.info("This is the ML Model")
        st.dataframe(compare_clf)
    
    from pycaret.regression import *    
    # Regression Model
    btn3 = st.button('Regression')

    # Run PyCaret to build a regression model and display the report
    if btn3:
        setup(df, target=target_column)
        reg_setup = pull()
        st.info("This is the ML Experiment settings")
        st.dataframe(reg_setup)
        
        st.subheader("Best Regression Model")
        reg_best_model = compare_models()
        compare_reg =  pull()
        st.info("This is the ML Model")
        st.dataframe(compare_reg)