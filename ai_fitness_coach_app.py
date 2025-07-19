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
        st.success("✅ Workout saved! You’re building something awesome.")

def show_weekly_plan():
    st.subheader("📅 Weekly Workout Plan")
    st.image(IMAGE_URL, use_container_width=True)
    for day, plan in DEFAULT_WEEKLY_PLAN.items():
        st.write(f"**{day}**: {plan} — Stay consistent, prioritize form, and listen to your body.")

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
        st.success("💪 Great consistency! Keep pushing, champ.")
    elif 2 <= count < 4:
        st.info("You’re on the path — try to hit 4+ sessions next week.")
    else:
        st.error("Let’s get moving again — even a short session counts!")

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
        st.success("🍏 Meals saved! Here's your AI coach's feedback:")

        all_meals = " ".join([breakfast, snack, lunch, dinner]).lower()

        if "candy" in all_meals or "soda" in all_meals or "chips" in all_meals:
            st.warning("🚨 Cut back on sugary and processed foods. Replace them with fruit, nuts, or yogurt.")
        elif "fruit" in all_meals or "vegetable" in all_meals or "chicken" in all_meals or "egg" in all_meals:
            st.success("✅ Clean eating! You’re fueling your body right.")
        elif "bread" in all_meals or "rice" in all_meals:
            st.info("🟡 Try switching to whole grain versions for more fiber and energy.")
        else:
            st.info("ℹ️ Try adding protein, fiber, and colorful veggies to your meals for a complete diet.")

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
        st.success("📊 Stats saved! You’re one step closer to your goal.")

def ai_suggestions():
    st.subheader("🧠 AI Suggestions")
    st.image(IMAGE_URL, use_container_width=True)
    st.markdown("""
    - Based on your activity, aim for **7–8 hours of sleep** each night.
    - Consider **adding stretching** before bed to recover faster.
    - If you’re tired mid-week, **do an active recovery** day instead of pushing through.
    - Track your meals — small changes (like swapping white bread for whole grain) can make a big difference.
    - Hydration tip: drink water **30 mins before meals** and reduce sugary drinks.
    """)

def motivation_corner():
    st.subheader("🔥 Motivation Corner")
    st.image(IMAGE_URL, use_container_width=True)
    st.markdown("""
    - “You don’t have to be extreme, just consistent.”
    - “It’s you vs. you — no one else.”
    - “Every rep counts. Every step matters.”
    - “Progress > Perfection.”
    - “Your future self is watching. Make them proud.”  
    """)
    st.info("Whenever you feel lazy, come back here for a boost.")

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
