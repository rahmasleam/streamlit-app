# importing libraries
import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px

# loading data
df = pd.read_csv('D:/After Graduate/Electropi/Streamlit/dataset/company_sales_data.csv')
st.write(df.head())

# matplotlib
st.header("Matplotlib")

st.subheader("Line Plot")
fig = plt.figure(figsize=(15,8))
plt.plot(df['month_number'], df['total_profit'], c='r', lw =5, marker='^', markersize=10, ls ='--')
plt.title("Month vs. Profit", fontsize=20)
plt.xlabel("Months")
plt.ylabel('Profit')
st.pyplot(fig)

st.text('This is a text descripting the previous figure')

st.subheader("scatter Plot")
fig = plt.figure(figsize=(15,8))
plt.scatter(df['month_number'], df['total_profit'])
plt.title("Month vs. Profit", fontsize=20)
plt.xlabel("Months")
plt.ylabel('Profit')
st.pyplot(fig)

df_1 = sns.load_dataset('tips')
st.dataframe(df_1.head())

st.subheader("histogram")
fig = plt.figure(figsize=(15,8))
sns.histplot(df_1['total_bill'])
st.pyplot(fig)

st.subheader("Histogram (distplot)")
fig = plt.figure(figsize=(15,8))
sns.distplot(df_1['total_bill'])
st.pyplot(fig)

st.subheader("scatter Plot")
fig = plt.figure(figsize=(15,8))
options = st.selectbox("Select an option", ['sex','smoker','day','time'])
sns.scatterplot(data=df_1, x=df_1['total_bill'], y=df_1['tip'], hue=options)
st.pyplot(fig)

st.subheader("Box Plot")
fig = plt.figure(figsize=(15,8))
options = st.radio("Select an option", ['total_bill','tip'])
sns.boxplot(data=df_1, y=options)
st.pyplot(fig)

st.subheader("Heatmap")
fig = plt.figure(figsize=(15,8))
sns.heatmap(df_1.corr(), annot=True)
st.pyplot(fig)

st.header("Plotly")

st.subheader("Scatter Plot")
options = st.selectbox("Select an option", ['sex','smoker','day','time'], key ="A")
fig = px.scatter(data_frame=df_1, x='total_bill', y='tip', color=options)
st.plotly_chart(fig)

st.subheader('Bar Chart')
fig = px.bar(df_1['sex'])
fig_1 = px.bar(data_frame=df_1, x=df_1['smoker'], color='sex')
st.plotly_chart(fig)
st.plotly_chart(fig_1)

st.subheader("Histogram")
fig = px.histogram(df_1['tip'])
st.plotly_chart(fig)

st.subheader("Violin Plot")
fig = px.violin(df_1['total_bill'])
st.plotly_chart(fig)
