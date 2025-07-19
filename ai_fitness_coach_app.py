ai_fitness_coach_app.py

import streamlit as st
import datetime
import json
import os
import matplotlib.pyplot as plt
from PIL import Image
import urllib.request

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

NUTRITION_TIPS = [
    "Drink at least 2L of water daily to stay hydrated.",
    "Focus on whole foods like fruits, vegetables, and lean proteins.",
    "Avoid sugary drinks and late-night snacks.",
    "Balance your meals with carbs, proteins, and healthy fats."
]

# --- Load and Save Functions ---
def load_data():
    if not os.path.exists(WORKOUT_FILE):
        return []
    with open(WORKOUT_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(WORKOUT_FILE, "w") as file:
        json.dump(data, file, indent=2)

# --- Logging ---
def log_workout():
    st.subheader("🏋️ Log a New Workout")
    st.write("Use this to record your workouts daily. Try to be specific about the type of workout, how long you did it, and any notes you want to keep.")
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

# --- Weekly Plan ---
def show_weekly_plan():
    st.subheader("📅 Weekly Workout Plan")
    st.write("Below is your general weekly workout structure. Stay consistent and adjust if needed!")
    for day, plan in DEFAULT_WEEKLY_PLAN.items():
        st.write(f"**{day}**: {plan}")

# --- Progress Analyzer (AI Agent logic here) ---
def analyze_progress():
    st.subheader("📊 Progress Report")
    st.write("We've analyzed your progress. Here's what you've achieved recently and a suggestion for your next focus.")
    data = load_data()
    if not data:
        st.warning("No workouts logged yet.")
        return
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    count = sum(1 for entry in data if datetime.datetime.strptime(entry["date"], "%Y-%m-%d").date() >= last_week)
    st.write(f"You worked out **{count}** time(s) in the last 7 days.")

    if count >= 4:
        st.success("💪 Great consistency! Keep up the strong routine!")
    elif 2 <= count < 4:
        st.info("🙂 Doing okay — aim for 4+ workouts next week.")
    else:
        st.error("😢 Step it up — even 20 minutes counts!")

    # AI Agent Suggestion
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    suggestion = DEFAULT_WEEKLY_PLAN[tomorrow.strftime("%A")]
    st.info(f"📅 Tomorrow's Recommendation: **{suggestion}**")

# --- Gallery ---
def photo_gallery():
    st.subheader("📸 Fitness Inspiration")
    st.write("Check out these motivating images and sample exercise visuals to help you stay focused.")

    # Load image from web (replace with working links or local images if needed)
    image_urls = [
        "https://images.unsplash.com/photo-1599059811194-c9fa4f2d077b",
        "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b"
    ]
    for url in image_urls:
        try:
            image = Image.open(urllib.request.urlopen(url))
            st.image(image, use_container_width=True)
        except:
            st.warning("Image could not be loaded.")

# --- Nutrition Tips ---
def nutrition_tips():
    st.subheader("🥗 Nutrition Tips")
    st.write("Eat smart! Fuel your workouts with protein, healthy fats, and slow carbs. Here's a daily tip:")
    index = datetime.date.today().day % len(NUTRITION_TIPS)
    st.info(NUTRITION_TIPS[index])

# --- Streamlit Layout ---
st.title("🤖 AI Fitness Coach")

option = st.sidebar.selectbox(
    "Choose an option:",
    ("Log Workout", "Show Weekly Plan", "Analyze Progress", "Photo Gallery", "Nutrition Tips")
)

if option == "Log Workout":
    log_workout()
elif option == "Show Weekly Plan":
    show_weekly_plan()
elif option == "Analyze Progress":
    analyze_progress()
elif option == "Photo Gallery":
    photo_gallery()
elif option == "Nutrition Tips":
    nutrition_tips()
