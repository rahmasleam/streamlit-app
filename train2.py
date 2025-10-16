import streamlit as st
import pandas as pd 
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

from pycaret.regression import *

from pycaret.classification import *

@st.cache_resource
def load_data(file):
    df = pd.read_csv(file)
    return df

def main():
    st.title("AutoML")
    # st.sidebar.write('[Author: Rahma](%s)')
    st.sidebar.markdown(
        "## ***This web app is a No-Code tool for Exploratory Data Analysis and building Machine Learning model for Regression and Calssification tasks.***\n"
        "1. Load your dataset file (CSV file):\n"
        "2. Click on *Profile Dataset* button in order to generate the pandas profiling of the dataset:\n"
        "3. Choose your target column:\n"
        "4. Choose the machine learning task (Regression or Classification):\n"
        "5. Click on *Run Modelling* in order to start the training process.:\n"
        "\n When the model is built, you can view the results like the pipline model, Residuals plot, ROC Curve, Confusion Matrix, Feature importance, etc.\n"
        "\n6. Download the Pipline model in your local computer."
    )

    file = st.file_uploader("Upload Your Dataset in csv Format", type=['csv'])

    if file is not None:
        df = load_data(file)
        st.dataframe(df.head())

        profile = st.button('Profile Dataset')
        if profile:
            profile_df = df.profile_report()
            st_profile_report(profile_df)

        target = st.selectbox("Select the target variable", df.columns)
        task = st.selectbox("Select a ML task", ['Regression', 'Classification'])

        if task == "Regression":
            if st.button("Run Modelling"):
                exo_reg = setup(df, target=target)
                model_reg = compare_models()
                save_model(model_reg,'best_reg_model')
                st.success("Regression Model Build Successfully!")

                # Results 
                st.write("Feature Importance ")
                plot_model(model_reg, plot = "feature", save = True)
                st.image('Feature Importance .png')

if __name__ == '__main__':
    main()