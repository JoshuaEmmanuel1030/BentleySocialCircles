import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize data storage for simplicity
if 'events' not in st.session_state:
    st.session_state.events = pd.DataFrame(columns=['Name', 'Date', 'Time', 'Interest', 'Description'])

# Custom CSS for styling, including hover effect for buttons
st.markdown("""
    <style>
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
        /* Style the submit button with a blue to white hover effect */
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

# Custom JavaScript for confirmation message on event creation
st.markdown("""
    <script>
        function showConfirmation() {
            alert('Event created successfully!');
        }
    </script>
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
        
        # Display a JavaScript alert upon successful event creation
        st.markdown('<script>showConfirmation()</script>', unsafe_allow_html=True)

# Display all events if any exist
st.write("---")
st.markdown('<div class="section-title">All Events</div>', unsafe_allow_html=True)
if not st.session_state.events.empty:
    for _, event in st.session_state.events.iterrows():
        st.markdown(f"""
            <div class="event-card">
                <div class="event-title">{event['Name']}</div>
                <div><strong>Date:</strong> {event['Date']}</div>
                <div><strong>Time:</strong> {event['Time']}</div>
                <div class="event-description">{event['Description']}</div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.write("No events created yet.")
