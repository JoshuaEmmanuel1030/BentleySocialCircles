import streamlit as st
import pandas as pd
from datetime import datetime
from sklearn.cluster import KMeans
import random

# Initialize data storage
if 'events' not in st.session_state:
    st.session_state.events = pd.DataFrame(columns=['Name', 'Date', 'Time', 'Interest', 'Description'])

if 'user_interactions' not in st.session_state:
    # Simulated user interactions for recommendation system
    st.session_state.user_interactions = pd.DataFrame(columns=['User', 'Event', 'Interest'])

# Custom CSS and JS for styling
st.markdown("""
    <style>
        /* Custom styling for the app */
        body {
            font-family: Arial, sans-serif;
        }
        .title {
            font-size: 32px;
            color: #4A90E2;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        .section-title {
            font-size: 24px;
            color: #333333;
            margin-top: 40px;
        }
        .event-card {
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 20px;
            background-color: #F9F9F9;
        }
        .event-title {
            font-weight: bold;
            font-size: 18px;
            color: #333333;
        }
        .event-description {
            font-size: 14px;
            color: #666666;
        }
        /* Button hover effect */
        .stButton > button {
            background-color: #4A90E2;
            color: white;
            transition: background-color 0.3s ease, color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: white;
            color: #4A90E2;
            border: 1px solid #4A90E2;
        }
    </style>
""", unsafe_allow_html=True)

# Application title and description
st.markdown('<div class="title">Bentley Social Circles</div>', unsafe_allow_html=True)
st.write("Connect with the Bentley community by joining or creating meet-ups based on shared interests.")

# Sidebar: User interests selection
st.sidebar.header("Explore Events by Interest")
interests = ["Book Club", "Yoga", "Study Group", "Music", "Cooking", "Fitness", "Mental Health"]
selected_interests = st.sidebar.multiselect("Select interests to find matching events:", interests)

# Display relevant events
st.markdown('<div class="section-title">Available Events</div>', unsafe_allow_html=True)
if selected_interests:
    filtered_events = st.session_state.events[st.session_state.events['Interest'].isin(selected_interests)]
    if not filtered_events.empty:
        for _, event in filtered_events.iterrows():
            st.markdown(f"""
                <div class="event-card">
                    <div class="event-title">{event['Name']}</div>
                    <div><strong>Date:</strong> {event['Date']}</div>
                    <div><strong>Time:</strong> {event['Time']}</div>
                    <div class="event-description">{event['Description']}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No events found for the selected interests.")
else:
    st.write("Please select an interest to view available events.")

# Section: Create an Event
st.markdown('<div class="section-title">Create a New Event</div>', unsafe_allow_html=True)

with st.form("event_form"):
    name = st.text_input("Event Name")
    date = st.date_input("Date", min_value=datetime.today())
    time = st.time_input("Time")
    interest = st.selectbox("Interest", interests)
    description = st.text_area("Event Description")
    submit_button = st.form_submit_button("Create Event")

    if submit_button:
        # Append new event to the session state events DataFrame
        new_event = pd.DataFrame({
            "Name": [name],
            "Date": [date.strftime('%Y-%m-%d')],
            "Time": [time.strftime('%H:%M')],
            "Interest": [interest],
            "Description": [description]
        })
        st.session_state.events = pd.concat([st.session_state.events, new_event], ignore_index=True)
        st.success("Event created successfully!")

# Simulating user interactions with a function
def simulate_user_interaction(user, event, interest):
    new_interaction = pd.DataFrame({
        "User": [user],
        "Event": [event],
        "Interest": [interest]
    })
    st.session_state.user_interactions = pd.concat([st.session_state.user_interactions, new_interaction], ignore_index=True)

# Generate recommendations using clustering
def recommend_events(user_interest):
    if not st.session_state.user_interactions.empty:
        # Encoding interests for clustering
        interaction_data = st.session_state.user_interactions['Interest'].astype('category').cat.codes
        kmeans = KMeans(n_clusters=min(len(interests), len(st.session_state.user_interactions)), random_state=0)
        clusters = kmeans.fit_predict(interaction_data.values.reshape(-1, 1))
        st.session_state.user_interactions['Cluster'] = clusters

        # Recommend events based on user's interest cluster
        user_cluster = kmeans.predict([[user_interest]])
        recommended_events = st.session_state.events[st.session_state.events['Interest'].astype('category').cat.codes == user_cluster[0]]
        return recommended_events
    return pd.DataFrame()

# User Recommendation Section
st.write("---")
st.markdown('<div class="section-title">Recommended Events For You</div>', unsafe_allow_html=True)

user_interest = random.choice(interests)  # Simulating user interest input
recommended_events = recommend_events(user_interest)

if not recommended_events.empty:
    for _, event in recommended_events.iterrows():
        st.markdown(f"""
            <div class="event-card">
                <div class="event-title">{event['Name']}</div>
                <div><strong>Date:</strong> {event['Date']}</div>
                <div><strong>Time:</strong> {event['Time']}</div>
                <div class="event-description">{event['Description']}</div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.write("No recommendations available.")
