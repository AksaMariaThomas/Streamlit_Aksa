import streamlit as st
import pandas as pd

if "entries" not in st.session_state:
    st.session_state.entries = []

def get_status(minutes):
    return "Healthy" if int(minutes) >= 60 else "Needs More Me-Time"

st.title("🧠 Mental Wellness Logger")

with st.form("entry_form", clear_on_submit=True):
    name = st.text_input("Student Name")
    gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)
    activity = st.selectbox("Wellness Activity", ["Meditation", "Journaling", "Art", "Talking", "Social"])
    me_time = st.text_input("Me-Time Activity")
    screen_time = st.text_input("Screen-Free Time (in minutes)")

    submit = st.form_submit_button("Add Entry")

    if submit:
        if not name or not me_time or not screen_time:
            st.error("All fields are required.")
        elif not screen_time.isdigit() or int(screen_time) <= 0:
            st.error("Screen-Free Time must be a positive number.")
        else:
            status = get_status(screen_time)
            entry = {
                "Name": name,
                "Gender": gender,
                "Activity": activity,
                "Me-Time": me_time,
                "Screen-Free Time": int(screen_time),
                "Status": status
            }
            st.session_state.entries.append(entry)
            st.success("Entry added successfully!")

if st.session_state.entries:
    df = pd.DataFrame(st.session_state.entries)
    st.subheader("📋 All Entries")
    st.dataframe(df, use_container_width=True)
else:
    st.info("No entries yet.")
