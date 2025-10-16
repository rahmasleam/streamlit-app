import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query import *

from bokeh.plotting import figure
from bokeh.models import Legend
import altair as alt

st.set_page_config(page_title = "Dashboard", layout = 'wide')
st.title('Dashboard')
st.markdown("##")


        # ============================================================================================================================================ #

# Question 1 in Task 1
df = view_all_data("SELECT * FROM users")
# df = pd.DataFrame(result, columns=['user_id', 'subscribed', 'subscription_date', 'coupon', 'registration_date', 'last_edit_date', 'level', 'gender', 'age', 'study_degree', '10k_AI_initiative'])
df['subscription_date'] = pd.to_datetime(df['subscription_date'])

# Create a new DataFrame to count the number of subscribed users
# Sidebar for selecting the time interval (daily, weekly, monthly, yearly)
# st.sidebar.header("Please filter")
st.sidebar.title("Analytics Dashboard depend on users")
st.subheader("Count number of users registered ")
time_interval = st.selectbox("Choose Time Interval", ['', "Daily", "Weekly", "Monthly", "Yearly"], key = "selectbox_1")

# Filter the data based on the selected time interval
if time_interval == "Daily":
    registration_date = df.groupby(pd.Grouper(key= 'registration_date', freq = 'D'))['user_id'].count().rename('daily_count')
elif time_interval == "Weekly":
    registration_date = df.groupby(pd.Grouper(key= 'registration_date', freq = 'W'))['user_id'].count().rename('weekly_count')
elif time_interval == "Monthly":
    registration_date = df.groupby(pd.Grouper(key= 'registration_date', freq = 'M'))['user_id'].count().rename('monthly_count')
else:  # Yearly
    registration_date = df.groupby(pd.Grouper(key= 'registration_date', freq = 'Y'))['user_id'].count().rename('yearly_count')

if time_interval != '':
    st.write(f"Count number of registered by user_id: {time_interval}")
    # st.dataframe(registration_date)
    # st.line_chart(registration_date)
    st.bar_chart(registration_date)

# Create a new DataFrame to count the number of subscribed users
# st.sidebar.title("Select Time Interval")
st.subheader("Count number of users subscribed")
time_interval_1 = st.selectbox("Choose Time ", ['',"Daily", "Weekly", "Monthly", "Yearly"], key = "selectbox_2")

# Filter the data based on the selected time interval_1
if time_interval_1 == "Daily":
    subscription_date = df.groupby(pd.Grouper(key= 'subscription_date', freq = 'D'))['user_id'].count().rename('daily_count')
elif time_interval_1 == "Weekly":
    subscription_date = df.groupby(pd.Grouper(key= 'subscription_date', freq = 'W'))['user_id'].count().rename('weekly_count')
elif time_interval_1 == "Monthly":
    subscription_date = df.groupby(pd.Grouper(key= 'subscription_date', freq = 'M'))['user_id'].count().rename('monthly_count')
else:  # Yearly
    subscription_date = df.groupby(pd.Grouper(key= 'subscription_date', freq = 'Y'))['user_id'].count().rename('yearly_count')
if time_interval_1 != '':
    counts_df = pd.concat([subscription_date], axis=1).fillna(0)
    st.write(f"Count number of subscriped by user_id: {time_interval_1}")
    # st.dataframe(counts_df)
    # st.line_chart(counts_df)
    st.bar_chart(counts_df)

        # ============================================================================================================================================ #

## Question 2 in Task 1
df_1 = view_all_data("SELECT bundles.user_id,users.subscribed , users.subscription_date, bundles.creation_date FROM users JOIN bundles ON users.user_id = bundles.user_id")

st.subheader("Count number of subscribed users to bundles ")
time_interval_2 = st.selectbox("Choose Time ", ['',"Daily", "Weekly", "Monthly", "Yearly"], key = "selectbox_3")

# Filter the data based on the selected time interval_1
if time_interval_2 == "Daily":
    Freq = 'D'
elif time_interval_2 == "Weekly":
    Freq = 'W'
elif time_interval_2 == "Monthly":
    Freq = 'M'
else:  # Yearly
    Freq='Y'
if time_interval_2 != '':
    subscrip_bundle = df_1.groupby(['user_id', 'subscribed', pd.Grouper(key='creation_date', freq= Freq )]).size().reset_index(name='count')
    st.write(f"Count number of users subscribed to each bundle: {time_interval_2}")

    fig = px.area(subscrip_bundle, x='creation_date', y='count', color='subscribed', title="Subscription Trend over Time")
    st.plotly_chart(fig)

    # Visualize the data using a bar chart
    fig_1 = px.bar(subscrip_bundle, x='creation_date', y='count', color='subscribed',
                 title=f"Subscribed Users to Each Bundle ({time_interval})", labels={'count': 'Number of Users'})
    
    # Display the chart using st.plotly_chart
    st.plotly_chart(fig_1)

        # ============================================================================================================================================ #
### Question 3 in Task 1
df_2 = view_all_data("SELECT user_completed_courses.* , users.10k_AI_initiative FROM users JOIN user_completed_courses ON users.user_id = user_completed_courses.user_id JOIN courses ON user_completed_courses.course_id = courses.course_id WHERE users.10k_AI_initiative = 1")

def display_dashboard_10K():
    # Count the number of completed courses for each user
    completed_courses_count = df_2.groupby('user_id')['course_id'].count().reset_index(name='num_completed_courses')

    # Find information of the last completed course for each user
    last_completed_course_info = df_2.groupby('user_id').apply(lambda group: group.loc[group['completion_date'].idxmax()]).reset_index(drop=True)

    # Merge the two results
    merged_result = pd.merge(completed_courses_count, last_completed_course_info, on='user_id')

    # Drop unimportant columns
    merged_result.drop(columns=['course_id','10k_AI_initiative'],inplace=True)
    
    # Sorting descending then reset index
    merged_result.sort_values(by='num_completed_courses', ascending=False,inplace=True)
    merged_result.reset_index(drop='index',inplace=True)

    # Display the merged result

    st.subheader("Number of Completed Courses for Users in the 10k AI Initiative")
    st.dataframe(merged_result)

    # Bar chart using Altair
    st.subheader('Number of Completed Courses for Each User')
    chart = alt.Chart(merged_result).mark_bar().encode(
        x='user_id',
        y='num_completed_courses',
        tooltip=['user_id', 'num_completed_courses']
    ).properties(width=500)
    
    # Display the chart using st.altair_chart
    st.altair_chart(chart)

    # Scatter plot using Altair for relationship between completed courses and last completed course's degree
    st.markdown('#### Relationship Between Completed Courses and Last Completed Course\'s Degree')
    scatter_plot = alt.Chart(merged_result).mark_circle().encode(
        x='num_completed_courses',
        y='course_degree',
        color='course_degree',
        tooltip=['num_completed_courses', 'course_degree']
    ).properties(width=500)
    
    # Display the scatter plot
    st.altair_chart(scatter_plot)

# Streamlit app
st.sidebar.subheader('Users in the 10k AI initiative')

# Add a button to the sidebar
if st.sidebar.button('10k AI Initiative Dashboard'):
    display_dashboard_10K()

        # ============================================================================================================================================ #

#### Question 4 in Task 1
# number of their currently learning courses 
df_3 = view_all_data('SELECT user_courses.user_id, user_courses.course_id FROM user_courses LEFT JOIN user_completed_courses ON user_courses.user_id = user_completed_courses.user_id WHERE user_completed_courses.user_id IS NULL')

def current_learn_course():
    # Calculate the number of courses each user is currently learning
    users_learning_count = df_3.groupby('user_id')['course_id'].count().reset_index()
    users_learning_count.rename(columns={'course_id':'currently_learning_count'}, inplace=True)

    # Create a title for the dashboard
    st.title("Currently Learning Courses")

    # Display a table of all users and the number of their currently learning courses
    st.dataframe(users_learning_count)

    # Create a bar chart showing the number of courses each user is currently learning
    st.bar_chart(x='user_id', y='currently_learning_count', data=users_learning_count)

    # Create a histogram with Plotly
    fig = px.histogram(users_learning_count, x='currently_learning_count', title='Distribution of Currently Learning Courses')

    # Display the plot
    st.plotly_chart(fig)

# Streamlit app
st.sidebar.subheader('Count currently learning courses by users')

# Add a button to the sidebar
if st.sidebar.button('Currently Learning Dashboard'):
    current_learn_course()

# ======================================== ************************************ =================================

# number of completed courses through time
df_4 = view_all_data("SELECT user_completed_courses.* FROM user_completed_courses")

st.subheader("Count number of completed courses during time ")
time_interval_3 = st.selectbox("Choose Time ", ['',"Daily", "Weekly", "Monthly", "Yearly"], key = "selectbox_4")

# Filter the data based on the selected time interval_1
if time_interval_3 == "Daily":
    Freq = 'D'
elif time_interval_3 == "Weekly":
    Freq = 'W'
elif time_interval_3 == "Monthly":
    Freq = 'M'
else:  # Yearly
    Freq='Y'

if time_interval_3 != '':
    completed_user_course = df_4.groupby(['user_id', pd.Grouper(key='completion_date', freq= Freq)])['course_id'].count().reset_index()
    completed_user_course.rename(columns = {'course_id': 'num_completed_user_course' }, inplace=True)
    completed_user_course.sort_values(by='num_completed_user_course', ascending=False, inplace=True)
    completed_user_course.reset_index(drop='index', inplace=True)
    st.write(f"Count number of users subscribed to each bundle: {time_interval_3}")

    st.dataframe(completed_user_course)

    # Bar chart using Plotly Express
    fig = px.bar(completed_user_course, x='completion_date', y='num_completed_user_course', color='user_id',
                 title=f"Number of Completed Courses ({time_interval_3})", labels={'num_completed_user_course': 'Number of Courses'})
    
    # Display the chart using st.plotly_chart
    st.plotly_chart(fig)

        # ============================================================================================================================================ #

##### Question 5 in Task 1
# df_5 = view_all_data()


        # ============================================================================================================================================ #

###### Question 6 in Task 1
df_6 = view_all_data("SELECT capstone_evaluation_history.* FROM capstone_evaluation_history")
st.subheader("Count number of completed courses during time ")
with st.expander(" "):
    
    time_interval_3 = st.selectbox("Choose Time ", ['',"Daily", "Weekly", "Monthly", "Yearly"], key = "selectbox_4")

    # Filter the data based on the selected time interval_1
    if time_interval_3 == "Daily":
        Freq = 'D'
    elif time_interval_3 == "Weekly":
        Freq = 'W'
    elif time_interval_3 == "Monthly":
        Freq = 'M'
    else:  # Yearly
        Freq='Y'

    if time_interval_3 != '':
        completed_user_course = df_4.groupby(['user_id', pd.Grouper(key='completion_date', freq= Freq)])['course_id'].count().reset_index()
        completed_user_course.rename(columns = {'course_id': 'num_completed_user_course' }, inplace=True)
        completed_user_course.sort_values(by='num_completed_user_course', ascending=False, inplace=True)
        completed_user_course.reset_index(drop='index', inplace=True)
        st.write(f"Count number of users subscribed to each bundle: {time_interval_3}")

        st.dataframe(completed_user_course)

        # Bar chart using Plotly Express
        fig = px.bar(completed_user_course, x='completion_date', y='num_completed_user_course', color='user_id',
                    title=f"Number of Completed Courses ({time_interval_3})", labels={'num_completed_user_course': 'Number of Courses'})
        
        # Display the chart using st.plotly_chart
        st.plotly_chart(fig)


        # ============================================================================================================================================ #

####### Question 7 in Task 1
df_7 = view_all_data("SELECT capstones.*, capstone_evaluation_history.evaluation_date FROM capstones JOIN capstone_evaluation_history ON capstones.user_id = capstone_evaluation_history.user_id")

# Select specific columns 
df_7 = df_7.loc[:, ['user_id', 'course_id', 'chapter_id', 'lesson_id', 'degree', 'evaluation_date']]

# # Function to display the capstone evaluation dashboard
# st.subheader("Capstone Evaluation History")

# with st.expander("User's Capstone and Evaluation History"):
#     # Select a user from the available options
#     selected_user = st.selectbox("Select User", df_7['user_id'].unique())

#     # Filter data for the selected user
#     user_capstone_data = df_7[df_7['user_id'] == selected_user]

#     # Display the user's capstone and evaluation history
#     st.dataframe(user_capstone_data)

#     # Bar chart to visualize average evaluation degree for each course over time
#     fig = px.bar(user_capstone_data, x='evaluation_date', y='degree', color='course_id', title=f"Average Evaluation Degree Over Time for User {selected_user}'s Capstone",
#                     labels={'degree': 'Average Evaluation Degree'},
#                     category_orders={'course_id': sorted(user_capstone_data['course_id'].unique())})

#     # Display the chart using st.plotly_chart
#     st.plotly_chart(fig)

# # Function to display the capstone evaluation dashboard for a specific user
# def display_capstone_evaluation_dashboard(user_id):
#     st.subheader("Capstone Evaluation History")

#     with st.expander("User's Capstone and Evaluation History"):
#         # Filter data for the specified user_id
#         user_capstone_data = df_7[df_7['user_id'] == user_id]

#         # Display the user's capstone and evaluation history
#         st.dataframe(user_capstone_data)

#         # Bar chart to visualize average evaluation degree for each course over time
#         fig = px.bar(user_capstone_data, x='evaluation_date', y='degree', color='course_id', title=f"Average Evaluation Degree Over Time for User {user_id}'s Capstone",
#                      labels={'degree': 'Average Evaluation Degree'},
#                      category_orders={'course_id': sorted(user_capstone_data['course_id'].unique())})

#         # Display the chart using st.plotly_chart
#         st.plotly_chart(fig)

# # Streamlit app
# st.title('Capstone Evaluation Dashboard')
# st.sidebar.title('Sidebar Menu')

# # Manually input the desired user_id
# user_id_input = st.sidebar.number_input("Enter User ID")

# # Call the function with the specified user_id
# display_capstone_evaluation_dashboard(user_id_input)



# Function to display the capstone evaluation dashboard
st.subheader("Capstone Evaluation History")

with st.expander("User's Capstone and Evaluation History"):
    # Select a user from the available options
    selected_user = st.number_input("Enter User ID", value=1)

    # Filter data for the selected user
    user_capstone_data = df_7[df_7['user_id'] == selected_user]

    if not user_capstone_data.empty : 
        # Display the user's capstone and evaluation history
        st.dataframe(user_capstone_data)

        # Bar chart to visualize average evaluation degree for each course over time
        fig = px.bar(user_capstone_data, x='evaluation_date', y='degree', color='course_id', title=f"Average Evaluation Degree Over Time for User {selected_user}'s Capstone",
                        labels={'degree': 'Average Evaluation Degree'},
                        category_orders={'course_id': sorted(user_capstone_data['course_id'].unique())})

        # Display the chart using st.plotly_chart
        st.plotly_chart(fig)








# df_ = view_all_data()








df_users = view_all_data('SELECT users.* FROM users #1726')
df_bundles = view_all_data('SELECT bundles.bundle_id, bundles.if_used, bundles.creation_date FROM bundles')
df_courses = view_all_data('SELECT courses.* FROM courses')
df_completed_course = view_all_data('SELECT user_completed_courses.* FROM user_completed_courses')
df_user_lesson_history = view_all_data('SELECT user_lesson_history.user_id,  user_lesson_history.course_id, user_lesson_history.chapter_id, user_lesson_history.lesson_id, user_lesson_history.count, user_lesson_history.degree AS quizze_degree FROM user_lesson_history WHERE user_lesson_history.degree > 0 ')
df_capstone_evaluation_history = view_all_data('SELECT capstone_evaluation_history.* FROM capstone_evaluation_history WHERE capstone_evaluation_history.degree >= 60')
# using these dataframe and by streamlit Build a dashboard to allow us to search for a user id of a user and see the current user information, the user’s bundles, courses, completed courses, completed quizzes and degrees, and completed capstones with all details.




#  
#  #2157 
#  #16 
#  #667 
# #7372
# 

import streamlit as st
import pandas as pd



df_users = view_all_data('SELECT users.* FROM users #1726')
df_bundles = view_all_data('SELECT bundles.bundle_id, bundles.if_used, bundles.creation_date FROM bundles')
df_courses = view_all_data('SELECT courses.* FROM courses')
df_completed_course = view_all_data('SELECT user_completed_courses.* FROM user_completed_courses')
df_user_lesson_history = view_all_data('SELECT user_lesson_history.user_id,  user_lesson_history.course_id, user_lesson_history.chapter_id, user_lesson_history.lesson_id, user_lesson_history.count, user_lesson_history.degree AS quizze_degree FROM user_lesson_history WHERE user_lesson_history.degree > 0 ')
df_capstone_evaluation_history = view_all_data('SELECT capstone_evaluation_history.* FROM capstone_evaluation_history WHERE capstone_evaluation_history.degree >= 60')


# Function to display user information based on user ID
def display_user_info(user_id):
    st.subheader(f"User Information for User ID: {user_id}")

    # Display user information
    user_info = df_users[df_users['user_id'] == user_id]
    st.dataframe(user_info)

    # Display user's bundles
    user_bundles = df_bundles[df_bundles['user_id'] == user_id]
    st.subheader("User's Bundles")
    st.dataframe(user_bundles)

    # Display user's completed courses
    completed_courses = pd.merge(df_completed_course, df_courses, on='course_id', how='inner')
    user_completed_courses = completed_courses[completed_courses['user_id'] == user_id]
    st.subheader("User's Completed Courses")
    st.dataframe(user_completed_courses)

    # Display user's lesson history
    user_lesson_history = df_user_lesson_history[df_user_lesson_history['user_id'] == user_id]
    st.subheader("User's Lesson History")
    st.dataframe(user_lesson_history)

    # Display user's completed capstones
    user_completed_capstones = df_capstone_evaluation_history[df_capstone_evaluation_history['user_id'] == user_id]
    st.subheader("User's Completed Capstones")
    st.dataframe(user_completed_capstones)

# Streamlit app
st.title('User Information Dashboard')
st.sidebar.title('Search User')

# User input for user ID
user_id_input = st.sidebar.number_input("Enter User ID:", min_value=1, max_value=df_users['user_id'].max())

# Display user information when the user ID is input
if st.sidebar.button('Search'):
    # Create a new expander using st.expander
    with st.expander("User Information Page", expanded=True):
        display_user_info(user_id_input)

