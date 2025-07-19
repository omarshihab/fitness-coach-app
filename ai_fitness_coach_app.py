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

IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Gym_workout_equipment.jpg/640px-Gym_workout_equipment.jpg"

st.set_page_config(page_title="AI Fitness Coach", page_icon="💪", layout="centered")

# Sidebar branding
with st.sidebar:
    st.image(IMAGE_URL, caption="Train Smart, Stay Strong", use_column_width=True)
    st.title("🧠 Coach Menu")


def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as file:
        return json.load(file)

def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

def log_workout():
    st.subheader("🏋️ Log a New Workout")
    st.image(IMAGE_URL, use_container_width=True)
    workout_type = st.text_input("Workout Type (e.g., Chest Day, Cardio, Yoga)")
    duration = st.number_input("Duration (minutes)", min_value=0, step=5)
    notes = st.text_area("Details (sets, reps, weights, or feelings)")
    if st.button("Save Workout"):
        entry = {
            "date": str(datetime.date.today()),
            "workout_type": workout_type,
            "duration": duration,
            "notes": notes
        }
        data = load_data(WORKOUT_FILE)
        data.append(entry)
        save_data(WORKOUT_FILE, data)
        st.success("✅ Workout saved!")

def show_weekly_plan():
    st.subheader("📅 Weekly Workout Plan")
    st.image(IMAGE_URL, use_container_width=True)
    for day, plan in DEFAULT_WEEKLY_PLAN.items():
        st.write(f"**{day}**: {plan} — 💡 Keep intensity balanced and prioritize form over weight.")

def analyze_progress():
    st.subheader("📊 Weekly Progress")
    st.image(IMAGE_URL, use_container_width=True)
    data = load_data(WORKOUT_FILE)
    if not data:
        st.warning("No workouts logged yet.")
        return
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    count = sum(
        1 for entry in data
        if datetime.datetime.strptime(entry["date"], "%Y-%m-%d").date() >= last_week
    )
    st.write(f"You worked out **{count}** time(s) in the last 7 days.")
    if count >= 4:
        st.success("💪 Great consistency! You're on the right track.")
    elif 2 <= count < 4:
        st.info("You're doing okay — try aiming for at least 4 sessions.")
    else:
        st.error("Step it up next week. Let's build momentum together!")

def meal_log():
    st.subheader("🍽️ Meal Log & AI Feedback")
    st.image(IMAGE_URL, use_container_width=True)
    breakfast = st.text_input("Breakfast")
    snack = st.text_input("Snack")
    lunch = st.text_input("Lunch")
    dinner = st.text_input("Dinner")
    if st.button("Submit Meals"):
        meal_entry = {
            "date": str(datetime.date.today()),
            "breakfast": breakfast,
            "snack": snack,
            "lunch": lunch,
            "dinner": dinner
        }
        data = load_data(MEAL_FILE)
        data.append(meal_entry)
        save_data(MEAL_FILE, data)
        st.success("🍏 Meals saved! Here's your feedback:")

        all_meals = " ".join([breakfast, snack, lunch, dinner]).lower()

        if any(word in all_meals for word in ["candy", "soda", "chips", "fried"]):
            st.warning("🚫 Cut down on processed/sugary food. Try fruit, oats, or grilled meals instead.")
        elif any(word in all_meals for word in ["fruits", "vegetables", "chicken", "salmon", "eggs", "quinoa"]):
            st.success("✅ You're eating clean! Keep balancing protein, fiber, and healthy fats.")
        else:
            st.info("🧠 Add more whole foods: lean meats, leafy greens, nuts, oats. Avoid packaged stuff!")

def body_stats():
    st.subheader("📏 Body Stats & Goals")
    st.image(IMAGE_URL, use_container_width=True)
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.5)
    waist = st.number_input("Waist (cm)", min_value=0.0, step=0.5)
    goal = st.text_input("What's your main fitness goal? (e.g., lose weight, build muscle)")
    if st.button("Save Stats"):
        entry = {
            "date": str(datetime.date.today()),
            "weight": weight,
            "waist": waist,
            "goal": goal
        }
        data = load_data(BODY_STATS_FILE)
        data.append(entry)
        save_data(BODY_STATS_FILE, data)
        st.success("📊 Stats saved! Track changes weekly for best results.")

def ai_suggestions():
    st.subheader("🧠 AI Suggestions")
    st.image(IMAGE_URL, use_container_width=True)
    st.write("🔍 Based on your logs, here's what your virtual coach suggests:")
    st.markdown("- Add stretching before/after workouts to improve flexibility 🧘")
    st.markdown("- Include at least one rest day per week to avoid burnout 💤")
    st.markdown("- Try a new workout style every 2 weeks to stay motivated 🔁")

def motivation_corner():
    st.subheader("🔥 Motivation Corner")
    st.image(IMAGE_URL, use_container_width=True)
    st.write("💬 Here's your motivational quote of the day:")
    st.success("\"Push yourself, because no one else is going to do it for you.\" 💥")

# Streamlit layout
st.title("🤖 AI Fitness Coach")
st.image(IMAGE_URL, use_container_width=True)
option = st.sidebar.selectbox(
    "Choose an option:",
    (
        "Log Workout",
        "Show Weekly Plan",
        "Analyze Progress",
        "Meal Log & Feedback",
        "Body Stats & Goals",
        "AI Suggestions",
        "Motivation Corner"
    )
)

if option == "Log Workout":
    log_workout()
elif option == "Show Weekly Plan":
    show_weekly_plan()
elif option == "Analyze Progress":
    analyze_progress()
elif option == "Meal Log & Feedback":
    meal_log()
elif option == "Body Stats & Goals":
    body_stats()
elif option == "AI Suggestions":
    ai_suggestions()
elif option == "Motivation Corner":
    motivation_corner()
