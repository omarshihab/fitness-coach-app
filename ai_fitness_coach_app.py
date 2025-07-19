# ai_fitness_coach_app.py

import streamlit as st
import datetime
import json
import os
import matplotlib.pyplot as plt

WORKOUT_FILE = "fitness_log.json"
MEAL_FILE = "meal_log.json"
BODY_STATS_FILE = "body_stats.json"

DEFAULT_WEEKLY_PLAN = {
    "Monday": "Push (Chest, Shoulders, Triceps)",
    "Tuesday": "Pull (Back, Biceps)",
    "Wednesday": "Rest or Cardio",
    "Thursday": "Legs (Quads, Glutes, Calves)",
    "Friday": "Upper Body Mix",
    "Saturday": "Core + Cardio",
    "Sunday": "Rest"
}

IMAGES = {
    "Log Workout": "https://i.imgur.com/LgrvM8A.jpg",
    "Show Weekly Plan": "https://i.imgur.com/E5ZC1VY.jpg",
    "Analyze Progress": "https://i.imgur.com/yP1C8Sg.jpg",
    "Meal Log & Feedback": "https://i.imgur.com/9OeQnPz.jpg",
    "AI Suggestions": "https://i.imgur.com/0yH0Ald.jpg",
    "Motivation Corner": "https://i.imgur.com/M5EYlIo.jpg",
    "Body Stats & Goals": "https://i.imgur.com/hZo7NlU.jpg"
}

def load_data(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)

def save_data(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def display_image(title):
    url = IMAGES.get(title)
    if url:
        st.image(url, use_container_width=True)

def log_workout():
    st.subheader("🏋️ Log a New Workout")
    display_image("Log Workout")
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
        data = load_data(WORKOUT_FILE)
        data.append(entry)
        save_data(data, WORKOUT_FILE)
        st.success("Workout saved!")

def show_weekly_plan():
    st.subheader("📅 Weekly Workout Plan")
    display_image("Show Weekly Plan")
    for day, plan in DEFAULT_WEEKLY_PLAN.items():
        st.write(f"**{day}**: {plan}")

def analyze_progress():
    st.subheader("📊 Weekly Progress")
    display_image("Analyze Progress")
    data = load_data(WORKOUT_FILE)
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

def log_meals():
    st.subheader("🍽️ Meal Log & Feedback")
    display_image("Meal Log & Feedback")
    meals = {}
    for meal in ["Breakfast", "Snack", "Lunch", "Dinner"]:
        meals[meal] = st.text_input(f"What did you have for {meal}?")
    if st.button("Analyze Meals"):
        healthy_keywords = ["fruit", "vegetable", "chicken", "fish", "salad", "rice", "water"]
        score = sum(any(word in meals[meal].lower() for word in healthy_keywords) for meal in meals)
        entry = {"date": str(datetime.date.today()), **meals}
        data = load_data(MEAL_FILE)
        data.append(entry)
        save_data(data, MEAL_FILE)
        if score >= 3:
            st.success("🥦 Great job! Your meals look healthy today.")
        elif 1 <= score < 3:
            st.info("Not bad! Add more fruits/veggies next time.")
        else:
            st.warning("Try to eat cleaner tomorrow — you got this!")

def ai_suggestions():
    st.subheader("🧠 AI Suggestions")
    display_image("AI Suggestions")
    workout_data = load_data(WORKOUT_FILE)
    meal_data = load_data(MEAL_FILE)
    recent_workouts = len([w for w in workout_data if datetime.datetime.strptime(w["date"], "%Y-%m-%d").date() >= datetime.date.today() - datetime.timedelta(days=7)])
    recent_meals = meal_data[-1] if meal_data else {}

    if recent_workouts < 2:
        st.warning("You haven’t trained much this week. Try to do 3–4 days!")
    else:
        st.success("Solid workout streak! Keep it up.")

    if recent_meals:
        if "salad" in str(recent_meals.values()).lower():
            st.success("Nice food choices recently — keep eating clean!")
        else:
            st.info("Try to include more veggies or protein in meals.")

def motivation_corner():
    st.subheader("💬 Motivation Corner")
    display_image("Motivation Corner")
    st.write("Sometimes all you need is a little push!")
    st.info("""
    "Don't limit your challenges — challenge your limits."
    "Success starts with self-discipline."
    "You're one workout away from a good mood."
    "Small progress is still progress."
    "Consistency is key."
    """
    )

def body_stats():
    st.subheader("📏 Body Stats & Goals")
    display_image("Body Stats & Goals")
    weight = st.number_input("Current Weight (kg)", min_value=0.0)
    waist = st.number_input("Waist Circumference (cm)", min_value=0.0)
    goal = st.text_input("What’s your fitness goal?")
    if st.button("Save Stats"):
        entry = {
            "date": str(datetime.date.today()),
            "weight": weight,
            "waist": waist,
            "goal": goal
        }
        data = load_data(BODY_STATS_FILE)
        data.append(entry)
        save_data(data, BODY_STATS_FILE)
        st.success("Body stats and goals saved!")

st.set_page_config(page_title="AI Fitness Coach", layout="centered")
st.title("🤖 AI Fitness Coach")

option = st.sidebar.selectbox(
    "Choose an option:",
    (
        "Log Workout",
        "Show Weekly Plan",
        "Analyze Progress",
        "Meal Log & Feedback",
        "AI Suggestions",
        "Motivation Corner",
        "Body Stats & Goals"
    )
)

if option == "Log Workout":
    log_workout()
elif option == "Show Weekly Plan":
    show_weekly_plan()
elif option == "Analyze Progress":
    analyze_progress()
elif option == "Meal Log & Feedback":
    log_meals()
elif option == "AI Suggestions":
    ai_suggestions()
elif option == "Motivation Corner":
    motivation_corner()
elif option == "Body Stats & Goals":
    body_stats()
