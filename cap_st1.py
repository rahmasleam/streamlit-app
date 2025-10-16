import streamlit as st
import pandas as pd
import numpy as np
from pycaret.classification import *
from pycaret.regression import *

# Step 1: Upload dataset and detect column types and null values
st.title("Automated Data Preprocessing and Modeling")

uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Display the original dataset
    st.subheader("Original Dataset")
    st.write(df)

    # Step 2: Ask the user to select columns to drop and the target column
    st.subheader("Select Columns to Drop and the Target Column")

    # Let the user select columns to drop
    columns_to_drop = st.multiselect("Select columns to drop", df.columns)

    # Remove the selected columns
    df = df.drop(columns=columns_to_drop)

    # Let the user select the target column
    target_column = st.selectbox("Select the target column", df.columns)

    # Step 3: Detect the target column data type and task type
    target_dtype = df[target_column].dtype
    task_type = "classification" if target_dtype == "object" else "regression"

    # Step 4: Data preprocessing options
    st.subheader("Data Preprocessing Options")
    for column in df.columns:
        if column != target_column:
            preprocess_categorical = st.selectbox(
                f"Preprocess '{column}' (Categorical)",
                ["None", "Most Frequent", "Additional Class for Missing"],
            )
            preprocess_continuous = st.selectbox(
                f"Preprocess '{column}' (Continuous)",
                ["None", "Mean", "Median", "Mode"],
            )
            # Implement preprocessing based on user choices

    # Step 5: Run PyCaret to build a model and display the report
    st.subheader("PyCaret Model Building")

    if task_type == "classification":
        clf_setup = setup(df, target=target_column)
        clf_best_model = compare_models()

        # Display the best classification model
        st.subheader("Best Classification Model")
        st.write(clf_best_model)

    elif task_type == "regression":
        reg_setup = setup(df, target=target_column)
        reg_best_model = compare_models()

        # Display the best regression model
        st.subheader("Best Regression Model")
        st.write(reg_best_model)

    # Step 6: Plot the model
    st.subheader("Model Evaluation Plots")
    if task_type == "classification":
        plot_model(clf_best_model, plot="confusion_matrix")

    elif task_type == "regression":
        plot_model(reg_best_model, plot="residuals")

