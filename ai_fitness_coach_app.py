# ai_fitness_coach_app.py

import streamlit as st
import datetime
import json
import os
import random
import matplotlib.pyplot as plt

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
MOTIVATION_IMAGES = [
    "https://i.imgur.com/Z5dWg9U.jpeg",
    "https://i.imgur.com/OB0y6MR.jpeg",
    "https://i.imgur.com/1ZQz0dF.jpeg"
]
QUOTES = [
    "Push yourself, because no one else is going to do it for you.",
    "The body achieves what the mind believes.",
    "Success starts with self-discipline."
]
TIPS = [
    "Drink at least 2L of water daily.",
    "Eat protein with every meal to support muscle growth.",
    "Don't skip rest days — recovery builds strength."
]

def load_data():
    if not os.path.exists(WORKOUT_FILE):
        return []
    with open(WORKOUT_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(WORKOUT_FILE, "w") as file:
        json.dump(data, file, indent=2)

def log_workout():
    st.subheader("\U0001F4AA Log a New Workout")
    workout_type = st.text_input("Workout Type")
    duration = st.number_input("Duration (minutes)", min_value=0, step=5)
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
        st.success("Workout saved!")

def show_weekly_plan():
    st.subheader("\U0001F4C5 Weekly Workout Plan")
    for day, plan in DEFAULT_WEEKLY_PLAN.items():
        st.write(f"**{day}**: {plan}")

def analyze_progress():
    st.subheader("\U0001F4CA Weekly Progress")
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
        st.success("\U0001F4AA Great consistency!")
    elif 2 <= count < 4:
        st.info("Doing okay — try to aim for 4+ workouts.")
    else:
        st.error("Step it up next week — you got this!")

def ai_recommendation():
    st.subheader("\U0001F916 Smart Recommendation")
    data = load_data()
    if not data:
        st.info("Log some workouts first.")
        return
    today = datetime.date.today().strftime("%A")
    st.write(f"Today is **{today}**.")
    plan = DEFAULT_WEEKLY_PLAN.get(today, "Rest")
    st.write(f"Suggested focus: **{plan}**")

def motivation_boost():
    st.subheader("\U0001F3CB Motivation Boost")
    img_url = random.choice(MOTIVATION_IMAGES)
    quote = random.choice(QUOTES)
    st.image(img_url, use_container_width=True)
    st.markdown(f"> *{quote}*")

def workout_history():
    st.subheader("\U0001F4D3 Workout History")
    data = load_data()
    if not data:
        st.warning("No workouts yet.")
        return
    for entry in reversed(data):
        st.write(f"**{entry['date']}** — {entry['workout_type']} for {entry['duration']} mins")
        if entry['notes']:
            st.caption(entry['notes'])

def nutrition_tip():
    st.subheader("\U0001F34E Nutrition Tip")
    st.info(random.choice(TIPS))

def progress_chart():
    st.subheader("\U0001F4C8 Workout Minutes Chart")
    data = load_data()
    if not data:
        st.warning("No data yet.")
        return
    day_totals = {}
    for entry in data:
        date = entry['date']
        day_totals[date] = day_totals.get(date, 0) + entry['duration']
    sorted_days = sorted(day_totals)
    minutes = [day_totals[day] for day in sorted_days]
    plt.figure(figsize=(10, 4))
    plt.plot(sorted_days, minutes, marker='o')
    plt.xticks(rotation=45)
    plt.ylabel("Minutes")
    plt.title("Workout Duration Over Time")
    st.pyplot(plt)

# --- Streamlit Page ---
st.set_page_config(page_title="AI Fitness Coach", layout="wide")
st.title("\U0001F9B8 AI Fitness Coach")
option = st.sidebar.selectbox(
    "Choose an option:",
    (
        "Log Workout",
        "Show Weekly Plan",
        "Analyze Progress",
        "AI Recommendation",
        "Motivation Boost",
        "Workout History",
        "Nutrition Tip",
        "Progress Chart"
    )
)

if option == "Log Workout":
    log_workout()
elif option == "Show Weekly Plan":
    show_weekly_plan()
elif option == "Analyze Progress":
    analyze_progress()
elif option == "AI Recommendation":
    ai_recommendation()
elif option == "Motivation Boost":
    motivation_boost()
elif option == "Workout History":
    workout_history()
elif option == "Nutrition Tip":
    nutrition_tip()
elif option == "Progress Chart":
    progress_chart()
