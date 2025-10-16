import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px

# Upload data
st.header('Uploadind Data ')
with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.file_uploader("Upload your data file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
  # Read the data from the file
  #data = pd.read_csv(uploaded_file).encode("utf-8")

  # Check the file type
  if uploaded_file.name[-4:] == '.csv':
    df = pd.read_csv(uploaded_file)
    st.success("Data uploaded successfully!")
  elif uploaded_file.name[-5:] == '.xlsx'or uploaded_file.name[-4:] == '.xls':
    df = pd.read_excel(uploaded_file)
    st.success("Data uploaded successfully!")
  else:
    st.warning("Only CSV and XLSX files are supported.")

  # Show dataframe
  st.subheader('Loaded DataFrame :')
  st.dataframe(df)

  # # Preprocessing for data 
        
  # Identify the data types of each column.
  st.header('Data Preprocessing')
  type_col = df.dtypes
  #st.subheader('Data type of each column')

  st.markdown('### ***Type of DataFrame***')
  with st.expander("Column Types"):
      st.dataframe(type_col)
     
  # Preprocessing options
  st.markdown('## Data Cleaning')

  st.markdown('### ***Show Sum of NAs in DataFrame***')
  with st.expander("Show NA"):
      st.dataframe(df.isna().sum())


  # Handle missing values
  st.markdown('### ***Handle missing values***')
  fill_options = ["Data With NA","Mean", "Median", "FillNA with 0", "Drop NA"]

  # Get the user's choice
  fill_option = st.selectbox("How to fill NA values?", fill_options)

  if  fill_option == "Data With NA":
    # Data with NA
    data = df
  elif fill_option == "Mean":
    # Fill NA values with the mean
    data = df.fillna(df.mean, inplace=True)
  elif fill_option == "Median":
    # Fill NA values with the median
    data = df.fillna(df.median, inplace=True)
  elif fill_option == "0":
    # Fill NA values with 0
    data = df.fillna(0, inplace=True)
  elif fill_option == "Drop NA":
    # Drop rows with NA values
    data = df.dropna(inplace=True)

  # Encode categorical features.
  st.markdown('### Encode categorical features')
  for col in df.select_dtypes(include='object'):
      df[col] = df[col].astype('category')
  st.success("Done")

  with st.sidebar:
      x = st.selectbox('Name of Columns X',data.columns, key=1)
      y = st.selectbox('Name of Columns Y',data.columns, key=2)

  # Data Visualization
  st.header('Data Visualization')

  # Create a histogram of the data
  st.subheader('Histogram')
  fig = px.histogram(data, x = x)
  st.plotly_chart(fig)

  # Create a box plot of the data
  st.subheader('Box Plot')
  fig = px.box(data, x=x)
  st.plotly_chart(fig)

  # Create a line chart of the data
  st.subheader('Line Chart')
  fig = px.line(data, x= x , y=y)
  st.plotly_chart(fig)

  # Create a bar chart of the data
  st.subheader('Bar Chart')
  fig = px.bar(data, x=x, y=y)
  st.plotly_chart(fig)

  # Create a Heatmap of the data
  st.subheader("Heatmap")
  fig = plt.figure(figsize=(15,8))
  sns.heatmap(data.corr(), annot=True)
  st.pyplot(fig)

  # Create a seaborn visualization of the data
  sns.pairplot(data)
  st.pyplot()

  # Create a Violin Plot visualization of the data
  st.subheader("Violin Plot")
  fig = px.violin(data,x)
  st.plotly_chart(fig)

  # Create a Violin Plot visualization of the data
  st.subheader("Histogram (distplot)")
  fig = plt.figure(figsize=(15,8))
  sns.distplot(data[x])
  st.pyplot(fig)

  # Create a Scatter Plot visualization of the data
  st.subheader("Scatter Plot")
  fig = px.scatter(data_frame=data, x= x,color=y)
  st.plotly_chart(fig)

  # # Create a pie chart of the data
  # if ValueError :
  #    st.warning("could not convert string to float")
  # else:
  #   st.subheader("Pie Chart")
  #   # fig = px.pie(data, values=y, labels=x)
  #   # st.plotly_chart(fig)
  #   fig, ax = plt.subplots()
  #   ax.pie(data, labels = x,colors = y, autopct="%1.1f%%")
  #   st.pyplot(fig)

























else:
   st.write('')
