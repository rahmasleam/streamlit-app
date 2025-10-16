# importing libraries
import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px

# Loading data
st.markdown('# Analysis data')
st.header('Upload data: ')
file_path = st.file_uploader("Upload the data file")

# check if the file_path is a CSV or Excel file
if file_path is not None:
    if file_path.name[-4:] == '.csv':
        df = pd.read_csv(file_path)
        st.write('Data loaded successfully!')
    elif file_path.name[-5:] == '.xlsx' or file_path.name[-4:] == '.xls':
        df = pd.read_excel(file_path)
        st.write('Data loaded successfully!')
    # Display the data
    st.header('Loaded data: ')
    st.dataframe(df.head(5))

    # # Preprocessing for data 
    
    # Identify the data types of each column.
    type_col = df.dtypes
    st.header('Data type of each column')
    
    # # as column
    # st.dataframe(type_col)  

    # Not column 
    for col, dtype in type_col.items():
        st.write(f'{col}: {dtype}')
    # =======================================
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

# ---------------------------------------------------------

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

    st.subheader("Violin Plot")
    option = st.selectbox("Select Column", n_col, key = 7)
    fig = px.violin(df[option])
    st.plotly_chart(fig)

    
    if not (file_path.name[-4:] == '.csv' or  file_path.name[-5:] == '.xlsx' or  file_path.name[-4:] == '.xls'):
        st.error('File path must be a CSV or Excel file.')




