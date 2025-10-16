import streamlit as st
import pandas as pd


st.markdown('# My Own PyCaret')
st.header('Upload data: ')
file_path = st.file_uploader("Upload the data file")

if file_path is not None:
    if file_path.name[-4:] == '.csv':
        df = pd.read_csv(file_path)
        st.success('Data loaded successfully!')
    elif file_path.name[-5:] == '.xlsx' or file_path.name[-4:] == '.xls':
        df = pd.read_excel(file_path)
        df.to_excel('data.xlsx', index=None)
        st.write('Data loaded successfully!')
    elif not (file_path.name[-4:] == '.csv' or  file_path.name[-5:] == '.xlsx' or  file_path.name[-4:] == '.xls'):
        st.error('File path must be a CSV or Excel file.')

    if (file_path.name[-4:] == '.csv' or  file_path.name[-5:] == '.xlsx' or  file_path.name[-4:] == '.xls'):
        # Display the data
        st.header('Loaded data: ')
        st.dataframe(df.head(10))

        # Preprocess the data
        st.header("Preprocessing")
        st.subheader('Drop Columns')
        columns_to_drop = st.multiselect("Select columns to drop", options=df.columns)
        if columns_to_drop:
            df.drop(columns_to_drop, axis=1, inplace=True)
        st.subheader('Target Columns')
        target_col = st.selectbox("Select target column", options=df.columns)
        categorical_cols = df.select_dtypes(include="object").columns.tolist()
        numerical_cols = df.select_dtypes(exclude="object").columns.tolist()
        for col in df.columns:
            if df[col].isna().sum() > 0:
                if col in categorical_cols:
                    fill_technique = st.selectbox(
                        f"How to fill missing values in {col}", 
                        options=["Most frequent", "Additional class for missing value"]
                    )
                    if fill_technique == "Most frequent":
                        df[col].fillna(df[col].mode()[0], inplace=True)
                    else:
                        df[col].fillna("Missing", inplace=True)
                else:
                    fill_technique = st.selectbox(
                        f"How to fill missing values in {col}", 
                        options=["Mean", "Median", "Mode"]
                    )
                    if fill_technique == "Mean":
                        df[col].fillna(df[col].mean(), inplace=True)
                    elif fill_technique == "Median":
                        df[col].fillna(df[col].median(), inplace=True)
                    else:
                        df[col].fillna(df[col].mode()[0], inplace=True)
        st.subheader("Processed data:")
        st.dataframe(df)

        # Train models using PyCaret
        st.header("Model training")
        task_type = "Regression" if df[target_col].dtype != "object" else "Classification"

        if task_type == "Regression":
            from pycaret.regression import *
            st.subheader("Training regression models...")
            setup(df, target=target_col, session_id=123, preprocess=False)
            exp = pull()
            st.dataframe(exp)

            models = compare_models(fold=5)
            compare_reg =  pull()
            st.subheader("Final model performance report:")
            st.dataframe(compare_reg)

        else:
            from pycaret.classification import *
            st.subheader("Training classification models...")
            setup(df, target=target_col, session_id=123, preprocess=False)
            exp = pull()
            st.dataframe(exp)

            models = compare_models(fold=5)
            compare_reg =  pull()
            st.subheader("Final model performance report:")
            st.dataframe(compare_reg)
        
