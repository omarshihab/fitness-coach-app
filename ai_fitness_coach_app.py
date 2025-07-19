# ai_fitness_coach_app.py

import streamlit as st
import datetime
import json
import os

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
IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/e/e7/Gym_workout_equipment.jpg"


def load_data(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as file:
        return json.load(file)


def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)


st.title("🤖 AI Fitness Coach")
st.sidebar.header("Login")
username = st.sidebar.text_input("Enter your username")

if not username:
    st.warning("Please enter your username to continue.")
    st.stop()

# Define per-user filenames
user_workout_file = f"{username}_workout.json"
user_meal_file = f"{username}_meal.json"
user_stats_file = f"{username}_stats.json"
user_weekly_plan_file = f"{username}_plan.json"


def log_workout():
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
        data = load_data(user_workout_file)
        if not isinstance(data, list):
            data = []
        data.append(entry)
        save_data(user_workout_file, data)
        st.success("✅ Workout saved!")


def show_weekly_plan():
    st.subheader("📅 Weekly Workout Plan")
    plan_data = load_data(user_weekly_plan_file)
    if not plan_data:
        plan_data = DEFAULT_WEEKLY_PLAN
    for day, plan in plan_data.items():
        st.write(f"**{day}**: {plan} 💡")


def customize_weekly_plan():
    st.subheader("✏️ Customize Your Weekly Plan")
    updated_plan = {}
    for day in DEFAULT_WEEKLY_PLAN:
        updated_plan[day] = st.text_input(f"{day}'s Plan", value=DEFAULT_WEEKLY_PLAN[day])
    if st.button("Save Weekly Plan"):
        save_data(user_weekly_plan_file, updated_plan)
        st.success("✅ Weekly plan updated!")


def analyze_progress():
    st.subheader("📊 Weekly Progress")
    data = load_data(user_workout_file)
    if not isinstance(data, list) or not data:
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
        data = load_data(user_meal_file)
        if not isinstance(data, list):
            data = []
        data.append(meal_entry)
        save_data(user_meal_file, data)
        st.success("🍏 Meals saved! Here's your feedback:")

        all_meals = " ".join([breakfast, snack, lunch, dinner]).lower()

        if "candy" in all_meals or "soda" in all_meals:
            st.warning("⚠️ Try to cut back on sugary items — swap soda with water or fruit-infused drinks.")
        elif any(x in all_meals for x in ["fruits", "vegetables", "chicken", "salmon", "quinoa"]):
            st.success("✅ Great job! You're eating nutritious foods. Keep it up.")
        else:
            st.info("🥗 Try to include more proteins, fiber, and natural foods. Avoid processed snacks.")


def body_stats():
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
        data = load_data(user_stats_file)
        if not isinstance(data, list):
            data = []
        data.append(entry)
        save_data(user_stats_file, data)
        st.success("📊 Stats saved! Track changes weekly for best results.")


def ai_suggestions():
    st.subheader("🤖 AI Suggestions")
    st.write("This AI assistant helps guide your weekly goals based on consistency and input logs.")
    data = load_data(user_workout_file)
    if isinstance(data, list) and len(data) >= 5:
        st.info("🔥 You've been active! Add variation to your workouts to keep things fresh.")
    else:
        st.info("📅 Aim to build a routine. Start with 3x a week and build from there.")


def motivation_corner():
    st.subheader("🌟 Motivation Corner")
    st.markdown(
        """
        - "The only bad workout is the one that didn’t happen."
        - "Success starts with self-discipline."
        - "Little progress is still progress! Keep going."
        """
    )


# Sidebar
option = st.sidebar.selectbox(
    "Choose an option:",
    (
        "Log Workout",
        "Show Weekly Plan",
        "Customize Weekly Plan",
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
elif option == "Customize Weekly Plan":
    customize_weekly_plan()
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

