import streamlit as st
import mysql.connector
import pandas as pd

# Replace these placeholders with your actual database details
db_config = {
   "host": "localhost",
   "user": "root",
   "password": "",
   "database": "demo_database"
}

# Create a connection to the MySQL database
conn = mysql.connector.connect(**db_config)

# Create a cursor
cursor = conn.cursor()

def view_all_data(query):
    # Execute a SELECT query
    #query = "SELECT * FROM users"
    cursor.execute(query)

    # Fetch the results
    data = cursor.fetchall()
    # return data

    df = pd.DataFrame(data, columns=[i[0] for i in cursor.description])

    # Close the cursor and connection
    # cursor.close()
    # conn.close()

    # Now you have your data in a pandas DataFrame
    # print(df)

    return df