import streamlit as st
import pandas as pd
from datetime import datetime
from sklearn.cluster import KMeans
import random

# Initialize data storage
if 'events' not in st.session_state:
    st.session_state.events = pd.DataFrame(columns=['Name', 'Date', 'Time', 'Interest', 'Description'])

# Custom CSS and JavaScript for the big red button
st.markdown("""
    <style>
        /* Styling for the big red button */
        .big-red-button {
            background-color: #FF4C4C;
            color: white;
            width: 100px;
            height: 100px;
            border: none;
            border-radius: 50%;
            font-size: 40px;
            text-align: center;
            line-height: 1.5;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        .big-red-button:hover {
            transform: scale(1.1);
        }
        .big-red-button:focus {
            outline: none;
        }
    </style>
    <script>
        function scrollToCreateEvent() {
            document.getElementById("create-event").scrollIntoView({ behavior: 'smooth' });
        }
    </script>
""", unsafe_allow_html=True)

# Big red button with a cross in the middle
st.markdown("""
    <div style="display: flex; justify-content: center; margin: 20px;">
        <button class="big-red-button" onclick="scrollToCreateEvent()">+</button>
    </div>
""", unsafe_allow_html=True)

# Application title and description
st.title("Bentley Social Circles")
st.write("Connect with the Bentley community by joining or creating meet-ups based on shared interests.")

# Sidebar: User interests selection
st.sidebar.header("Explore Events by Interest")
interests = ["Book Club", "Yoga", "Study Group", "Music", "Cooking", "Fitness", "Mental Health"]
selected_interests = st.sidebar.multiselect("Select interests to find matching events:", interests)

# Display relevant events
st.header("Available Events")
if selected_interests:
    filtered_events = st.session_state.events[st.session_state.events['Interest'].isin(selected_interests)]
    if not filtered_events.empty:
        for _, event in filtered_events.iterrows():
            st.write(f"### {event['Name']}")
            st.write(f"**Date**: {event['Date']}")
            st.write(f"**Time**: {event['Time']}")
            st.write(f"**Description**: {event['Description']}")
            st.write("---")
    else:
        st.write("No events found for the selected interests.")
else:
    st.write("Please select an interest to view available events.")

# Create Event Section with the ID for scrolling
st.header("Create a New Event")
st.markdown('<div id="create-event"></div>', unsafe_allow_html=True)

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
