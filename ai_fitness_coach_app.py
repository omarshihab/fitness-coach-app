# ai_fitness_coach_app.py

import streamlit as st
import datetime
import json
import os

WORKOUT_FILE = "fitness_log.json"

DEFAULT_WEEKLY_PLAN = {
    "Monday": "Push (Chest, Shoulders, Triceps)",
    "Tuesday": "Pull (Back, Biceps)",
    "Wednesday": "Rest or Cardio",
    "Thursday": "Legs (Quads, Glutes, Calves)",
    "Friday": "Upper Body Mix",
    "Saturday": "Core + Cardio",
    "Sunday": "Rest"
}

def load_data():
    if not os.path.exists(WORKOUT_FILE):
        return []
    with open(WORKOUT_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(WORKOUT_FILE, "w") as file:
        json.dump(data, file, indent=2)

def log_workout():
    st.subheader("🏋️ Log a New Workout")
    col1, col2 = st.columns(2)
    workout_type = col1.selectbox("Workout Type", ["Push", "Pull", "Legs", "Cardio", "Core", "Full Body", "Other"])
    duration = col2.number_input("Duration (minutes)", min_value=0, step=5)
    notes = st.text_area("Notes (e.g., sets, reps, weight)")
    if st.button("Save Workout"):
        entry = {
            "date": str(datetime.date.today()),
            "workout_type": workout_type,
            "duration": duration,
            "notes": notes
        }
        data = load_data()
        data.append(entry)
        save_data(data)
        st.success("✅ Workout saved!")

def show_weekly_plan():
    st.subheader("📅 Weekly Workout Plan")
    for day, plan in DEFAULT_WEEKLY_PLAN.items():
        st.markdown(f"**{day}**: {plan}")
    st.image("https://cdn.pixabay.com/photo/2021/09/25/17/04/bodybuilding-6655036_1280.jpg", use_column_width=True)

def analyze_progress():
    st.subheader("📊 Weekly Progress")
    data = load_data()
    if not data:
        st.warning("No workouts logged yet.")
        return
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    count = sum(
        1 for entry in data
        if datetime.datetime.strptime(entry["date"], "%Y-%m-%d").date() >= last_week
    )
    st.write(f"You've worked out **{count}** time(s) in the last 7 days.")
    if count >= 4:
        st.success("💪 Great consistency!")
    elif 2 <= count < 4:
        st.info("Doing okay — try to aim for 4+ workouts.")
    else:
        st.error("Step it up next week — you got this!")

    # 🧠 Autonomous AI Agent: Smart Progress Coach
    suggest_from_agent(data)

def suggest_from_agent(data):
    today = datetime.date.today()
    week_data = [
        entry for entry in data
        if datetime.datetime.strptime(entry["date"], "%Y-%m-%d").date() >= today - datetime.timedelta(days=7)
    ]
    types_done = [entry["workout_type"].lower() for entry in week_data]
    suggestions = []

    if "legs" not in types_done:
        suggestions.append("🦵 Try not to skip leg day this week!")
    if "cardio" not in types_done:
        suggestions.append("❤️‍🔥 Add at least one cardio session to improve heart health.")
    if len(week_data) < 3:
        suggestions.append("📅 Let's aim for 3+ workouts this week!")

    if suggestions:
        st.markdown("---")
        st.subheader("🧠 Smart Progress Coach Suggestions")
        for tip in suggestions:
            st.info(tip)

# Streamlit page layout
st.set_page_config(page_title="AI Fitness Coach", layout="centered")
st.title("🤖 AI Fitness Coach")

option = st.sidebar.selectbox(
    "Choose an option:",
    ("Log Workout", "Show Weekly Plan", "Analyze Progress")
)

if option == "Log Workout":
    log_workout()
elif option == "Show Weekly Plan":
    show_weekly_plan()
elif option == "Analyze Progress":
    analyze_progress()

