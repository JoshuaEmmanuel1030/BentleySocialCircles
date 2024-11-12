import streamlit as st
import pandas as pd
from datetime import datetime

# Setting up data storage for simplicity
if 'events' not in st.session_state:
    st.session_state.events = pd.DataFrame(columns=['Name', 'Date', 'Time', 'Interest', 'Description'])

# App title and description
st.title("Bentley Social Circles")
st.write("Connect with the Bentley community by joining or creating meet-ups based on shared interests.")

# Section: User interests selection
st.sidebar.header("Explore Events by Interest")
interests = ["Book Club", "Yoga", "Study Group", "Music", "Cooking", "Fitness", "Mental Health"]
selected_interests = st.sidebar.multiselect("Select interests to find matching events:", interests)

# Display relevant events
st.subheader("Available Events")
if selected_interests:
    filtered_events = st.session_state.events[st.session_state.events['Interest'].isin(selected_interests)]
    if not filtered_events.empty:
        st.write(filtered_events)
    else:
        st.write("No events found for the selected interests.")
else:
    st.write("Please select an interest to view available events.")

# Section: Create an Event
st.subheader("Create a New Event")

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

# Display all events if any exist
st.write("---")
st.subheader("All Events")
if not st.session_state.events.empty:
    st.write(st.session_state.events)
else:
    st.write("No events created yet.")
