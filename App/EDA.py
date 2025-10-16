import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pandas.api.types import is_numeric_dtype, is_string_dtype

# Initialize session state for df
if 'df' not in st.session_state:
    st.session_state.df = None

st.markdown('# My Own PyCaret')
st.header('Upload data: ')
file_path = st.file_uploader("Upload the data file")

if file_path is not None:
    if file_path.name.endswith('.csv'):
        st.session_state.df = pd.read_csv(file_path)
        st.success('Data loaded successfully!')
    elif file_path.name.endswith(('.xlsx', '.xls')):
        st.session_state.df = pd.read_excel(file_path)
        st.success('Data loaded successfully!')
    else:
        st.error('File path must be a CSV or Excel file.')
        st.session_state.df = None

# Check if data is loaded
def check_df():
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a CSV or Excel file first!")
        st.stop()

if st.session_state.df is not None:
    df = st.session_state.df.copy()
    # Display the data
    st.header('Loaded data: ')
    st.dataframe(df.head(10))

    # Preprocess the data
    st.header("Preprocessing")
    st.subheader('Drop Columns')
    columns_to_drop = st.multiselect("Select columns to drop", options=df.columns)
    if columns_to_drop:
        df.drop(columns_to_drop, axis=1, inplace=True)
        st.session_state.df = df

    st.subheader('Target Column')
    target_col = st.selectbox("Select target column", options=df.columns)
    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    numerical_cols = df.select_dtypes(exclude="object").columns.tolist()

    # Handle missing values
    for col in df.columns:
        if df[col].isna().sum() > 0:
            if col in categorical_cols:
                fill_technique = st.selectbox(
                    f"How to fill missing values in {col}", 
                    options=["Most frequent", "Additional class for missing value"],
                    key=f"fill_cat_{col}"
                )
                if fill_technique == "Most frequent":
                    df[col].fillna(df[col].mode()[0], inplace=True)
                else:
                    df[col].fillna("Missing", inplace=True)
            else:
                fill_technique = st.selectbox(
                    f"How to fill missing values in {col}", 
                    options=["Mean", "Median", "Mode"],
                    key=f"fill_num_{col}"
                )
                if fill_technique == "Mean":
                    df[col].fillna(df[col].mean(), inplace=True)
                elif fill_technique == "Median":
                    df[col].fillna(df[col].median(), inplace=True)
                else:
                    df[col].fillna(df[col].mode()[0], inplace=True)
    st.subheader("Processed data:")
    st.dataframe(df)
    st.session_state.df = df

    # Visualization
    st.header("Data Visualization")
    n_col = list(df.columns)

    # Matplotlib/Seaborn Visualizations
    st.subheader("Matplotlib/Seaborn Visualizations")
    st.markdown("### Histogram")
    hist_col = st.selectbox("Select column for Histogram", n_col, key="hist_col")
    if is_numeric_dtype(df[hist_col]) or is_string_dtype(df[hist_col]):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data=df, x=hist_col, kde=True, ax=ax)
        st.pyplot(fig)
    else:
        st.warning(f"Column {hist_col} is not suitable for histogram.")

    st.markdown("### Box Plot")
    box_col = st.selectbox("Select column for Box Plot", n_col, key="box_col")
    if is_numeric_dtype(df[box_col]):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df, y=box_col, ax=ax)
        st.pyplot(fig)
    else:
        st.warning(f"Column {box_col} is not suitable for box plot.")

    st.markdown("### Correlation Heatmap")
    if numerical_cols:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df[numerical_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
    else:
        st.warning("No numerical columns available for correlation heatmap.")

    # Plotly Visualizations
    st.subheader("Plotly Interactive Visualizations")
    st.markdown("### Scatter Plot")
    scatter_x = st.selectbox("Select X-axis column", n_col, key="scatter_x")
    scatter_y = st.selectbox("Select Y-axis column", n_col, key="scatter_y")
    fig = px.scatter(data_frame=df, x=scatter_x, y=scatter_y, color=target_col if target_col in df.columns else None)
    st.plotly_chart(fig)

    st.markdown("### Bar Chart")
    bar_x = st.selectbox("Select X-axis column for Bar Chart", n_col, key="bar_x")
    fig = px.bar(data_frame=df, x=bar_x, color=target_col if target_col in df.columns else None)
    st.plotly_chart(fig)

    # Train models using PyCaret
    st.header("Model Training")
    task_type = "Regression" if is_numeric_dtype(df[target_col]) else "Classification"

    if task_type == "Regression":
        from pycaret.regression import *
        st.subheader("Training regression models...")
        with st.spinner('Models are being built...it will take time (2-5 minutes)'):
            setup(df, target=target_col, session_id=123, preprocess=False, silent=True)
            exp = pull()
            st.dataframe(exp)

            models = compare_models(fold=5)
            compare_reg = pull()
            st.subheader("Final model performance report:")
            st.dataframe(compare_reg)

    else:
        from pycaret.classification import *
        st.subheader("Training classification models...")
        with st.spinner('Models are being built...it will take time (2-5 minutes)'):
            setup(df, target=target_col, session_id=123, preprocess=False, silent=True)
            exp = pull()
            st.dataframe(exp)

            models = compare_models(fold=5)
            compare_clf = pull()
            st.subheader("Final model performance report:")
            st.dataframe(compare_clf)