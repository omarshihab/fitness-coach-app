# ai_fitness_coach_app.py

import streamlit as st
import datetime
import json
import os
import matplotlib.pyplot as plt

# File templates with user-based dynamic naming
def get_user_filename(base, username):
    return f"{base}_{username}.json"

DEFAULT_WEEKLY_PLAN = {
    "Monday": "Push (Chest, Shoulders, Triceps)",
    "Tuesday": "Pull (Back, Biceps)",
    "Wednesday": "Rest or Cardio",
    "Thursday": "Legs (Quads, Glutes, Calves)",
    "Friday": "Upper Body Mix",
    "Saturday": "Core + Cardio",
    "Sunday": "Rest"
}

# Load and save functions

def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as file:
        return json.load(file)

def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

# Each function accepts the username

def log_workout(username):
    st.subheader("🏋️ Log a New Workout")
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
        data = load_data(get_user_filename("fitness_log", username))
        data.append(entry)
        save_data(get_user_filename("fitness_log", username), data)
        st.success("✅ Workout saved!")

def show_weekly_plan():
    st.subheader("📅 Weekly Workout Plan")
    for day, plan in DEFAULT_WEEKLY_PLAN.items():
        st.write(f"**{day}**: {plan} — Keep intensity balanced and prioritize form over weight.")

def analyze_progress(username):
    st.subheader("📊 Weekly Progress")
    data = load_data(get_user_filename("fitness_log", username))
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

def meal_log(username):
    st.subheader("🍽️ Meal Log & AI Feedback")
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
        data = load_data(get_user_filename("meal_log", username))
        data.append(meal_entry)
        save_data(get_user_filename("meal_log", username), data)
        st.success("🍏 Meals saved! Here's your feedback:")

        all_meals = " ".join([breakfast, snack, lunch, dinner]).lower()

        feedback = []
        if any(word in all_meals for word in ["candy", "soda", "cake", "chips"]):
            feedback.append("⚠️ Try to cut back on sugary/junk foods — opt for water, fruits, or nuts instead.")
        if any(word in all_meals for word in ["vegetable", "fruit", "chicken", "salmon", "eggs"]):
            feedback.append("✅ Great job including nutrient-rich foods!")
        if "nothing" in all_meals or not all_meals.strip():
            feedback.append("😕 Remember to eat! Fueling your body is key.")
        if not feedback:
            feedback.append("ℹ️ Try to balance carbs, proteins, and healthy fats in each meal.")

        for line in feedback:
            st.write(line)

def body_stats(username):
    st.subheader("📏 Body Stats & Goals")
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
        data = load_data(get_user_filename("body_stats", username))
        data.append(entry)
        save_data(get_user_filename("body_stats", username), data)
        st.success("📊 Stats saved! Track changes weekly for best results.")

def ai_suggestions():
    st.subheader("🤖 AI Suggestions")
    st.write("Here are some personalized suggestions to boost your fitness journey:")
    st.markdown("- Try adding mobility/stretching sessions to improve recovery 🧘")
    st.markdown("- Schedule your workouts like meetings to stay consistent 📅")
    st.markdown("- Combine strength + cardio for balanced development 💥")

def motivation_corner():
    st.subheader("🔥 Motivation Corner")
    st.write("Need a boost? Here's your dose of encouragement:")
    st.success("""
    "Discipline is choosing between what you want now and what you want most."
    Keep pushing — you're stronger than you think 💪
    """)

# ---------------- App Layout -------------------
st.title("🏋️ AI Fitness Coach")

username = st.sidebar.text_input("Enter your name to get started")
if username:
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
        log_workout(username)
    elif option == "Show Weekly Plan":
        show_weekly_plan()
    elif option == "Analyze Progress":
        analyze_progress(username)
    elif option == "Meal Log & Feedback":
        meal_log(username)
    elif option == "Body Stats & Goals":
        body_stats(username)
    elif option == "AI Suggestions":
        ai_suggestions()
    elif option == "Motivation Corner":
        motivation_corner()
else:
    st.warning("👤 Please enter your name to access the app features.")
