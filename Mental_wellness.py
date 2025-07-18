import streamlit as st
import pandas as pd
import os

# File to store data
excel_file = "mental_wellness_basic.xlsx"

# Load entries from Excel
@st.cache_data
def load_data():
    if os.path.exists(excel_file):
        return pd.read_excel(excel_file)
    else:
        return pd.DataFrame(columns=["Name", "Gender", "Activity", "Me-Time", "Screen-Free Time", "Status"])

# Save entries to Excel
def save_data(df):
    df.to_excel(excel_file, index=False)

# Determine health status
def get_status(minutes):
    return "Healthy" if int(minutes) >= 60 else "Needs More Me-Time"

# Load data
df = load_data()

st.title("🧠 Mental Wellness Logger (Basic)")

# --- Input Form ---
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
            new_entry = pd.DataFrame([[name, gender, activity, me_time, int(screen_time), status]],
                                     columns=df.columns)
            df = pd.concat([df, new_entry], ignore_index=True)
            save_data(df)
            st.success("Entry added successfully!")

# --- Display Entries ---
st.subheader("📋 All Entries")
st.dataframe(df, use_container_width=True)
