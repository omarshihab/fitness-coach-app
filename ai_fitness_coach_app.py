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

MOTIVATIONAL_QUOTES = [
    "Push yourself, because no one else is going to do it for you.",
    "It never gets easier, you just get stronger.",
    "Don't limit your challenges, challenge your limits.",
    "You're only one workout away from a good mood."
]

PHOTOS = [
    "https://i.imgur.com/zYxDCQT.jpeg",
    "https://i.imgur.com/AsG1FYo.jpeg",
    "https://i.imgur.com/nLzj9tS.jpeg"
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
    st.subheader("🏋️ Log a New Workout")
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
    st.subheader("📅 Weekly Workout Plan")
    for day, plan in DEFAULT_WEEKLY_PLAN.items():
        st.write(f"**{day}**: {plan}")

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

    # Graph
    days = {}
    for entry in data:
        day = entry["date"]
        days[day] = days.get(day, 0) + 1
    if days:
        dates = list(days.keys())[-7:]
        freqs = [days[d] for d in dates]
        fig, ax = plt.subplots()
        ax.bar(dates, freqs, color="skyblue")
        plt.xticks(rotation=45)
        st.pyplot(fig, use_container_width=True)

def show_motivation():
    st.subheader("🔥 Daily Motivation")
    quote = random.choice(MOTIVATIONAL_QUOTES)
    st.info(f"📢 {quote}")

def ai_suggestions():
    st.subheader("🤖 AI Agent Suggestions")
    data = load_data()
    if not data:
        st.warning("Not enough data to give suggestions yet.")
        return
    recent = data[-3:]
    if all("legs" in w["workout_type"].lower() for w in recent):
        st.write("🦵 You've been doing a lot of leg workouts! Maybe give upper body some love.")
    elif all(w["duration"] < 30 for w in recent):
        st.write("⏱️ Try increasing your workout time for better results.")
    else:
        st.write("✅ Keep it up! You're training smart.")

def body_stats():
    st.subheader("📏 Body Stats & Goals")
    weight = st.number_input("Weight (kg)", 0.0)
    height = st.number_input("Height (cm)", 0.0)
    goal = st.text_input("Your fitness goal")
    if weight and height:
        bmi = weight / ((height / 100) ** 2)
        st.write(f"Your BMI is **{bmi:.2f}**")
    if goal:
        st.write(f"🎯 Goal: {goal}")

def nutrition_tips():
    st.subheader("🥗 Nutrition Assistant")
    data = load_data()
    total = len(data)
    if total == 0:
        st.write("Start logging workouts to receive personalized tips!")
    elif total < 3:
        st.write("Try adding more protein to fuel recovery.")
    else:
        st.write("Great job staying active! Balance your meals with complex carbs and lean protein.")

def photo_gallery():
    st.subheader("📸 Fitness Inspiration Gallery")
    for url in PHOTOS:
        st.image(url, caption="Stay motivated!", use_container_width=True)

def about_agent():
    st.subheader("🧠 About the AI Agent")
    st.markdown("""
    This AI Fitness Coach includes smart agents that:
    - Analyze your workout data to give **custom suggestions**.
    - Motivate you daily with quotes.
    - Help with nutrition advice based on activity.

    These AI tools help guide you automatically, like a personal trainer inside your app.
    """)

# Layout
st.title("🏋️ AI Fitness Coach App")
option = st.sidebar.selectbox(
    "🏋️‍♂️ Choose a section:",
    (
        "Log Workout",
        "Show Weekly Plan",
        "Analyze Progress",
        "Daily Motivation",
        "AI Suggestions",
        "Body Stats & Goals",
        "Nutrition Assistant",
        "Photo Gallery",
        "About the AI Agent"
    )
)

if option == "Log Workout":
    log_workout()
elif option == "Show Weekly Plan":
    show_weekly_plan()
elif option == "Analyze Progress":
    analyze_progress()
elif option == "Daily Motivation":
    show_motivation()
elif option == "AI Suggestions":
    ai_suggestions()
elif option == "Body Stats & Goals":
    body_stats()
elif option == "Nutrition Assistant":
    nutrition_tips()
elif option == "Photo Gallery":
    photo_gallery()
elif option == "About the AI Agent":
    about_agent()
