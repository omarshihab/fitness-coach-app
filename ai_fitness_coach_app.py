# ai_fitness_coach_app.py

import streamlit as st
import datetime
import json
import os

IMAGE_EMOJI = "🏋️"

# Save and load using username-based filenames
def get_filename(base, username):
    return f"{base}_{username}.json"

def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as file:
        return json.load(file)

def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

DEFAULT_WEEKLY_PLAN = {
    "Monday": "Push (Chest, Shoulders, Triceps)",
    "Tuesday": "Pull (Back, Biceps)",
    "Wednesday": "Rest or Cardio",
    "Thursday": "Legs (Quads, Glutes, Calves)",
    "Friday": "Upper Body Mix",
    "Saturday": "Core + Cardio",
    "Sunday": "Rest"
}

st.title("🤖 AI Fitness Coach")
username = st.sidebar.text_input("Enter your username to get started")

if not username:
    st.warning("Please enter your username.")
    st.stop()

# Filenames per user
WORKOUT_FILE = get_filename("fitness_log", username)
MEAL_FILE = get_filename("meal_log", username)
BODY_STATS_FILE = get_filename("body_stats", username)
WEEKLY_PLAN_FILE = get_filename("weekly_plan", username)

# Function to customize weekly plan
def customize_weekly_plan():
    st.subheader("📝 Customize Your Weekly Plan")
    user_plan = {}
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days:
        user_plan[day] = st.text_input(f"{day} Plan", DEFAULT_WEEKLY_PLAN.get(day, ""))
    if st.button("Save Weekly Plan"):
        save_data(WEEKLY_PLAN_FILE, user_plan)
        st.success("✅ Weekly plan saved!")

# Load user plan or fallback to default
try:
    weekly_plan = load_data(WEEKLY_PLAN_FILE)
except:
    weekly_plan = DEFAULT_WEEKLY_PLAN

def log_workout():
    st.subheader(f"{IMAGE_EMOJI} Log a New Workout")
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
    for day, plan in weekly_plan.items():
        st.write(f"**{day}**: {plan} — Stay consistent!")

def analyze_progress():
    st.subheader("📊 Weekly Progress")
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
        st.success("💪 Great consistency! Keep going.")
    elif 2 <= count < 4:
        st.info("You're doing okay — aim for 4+ workouts next week.")
    else:
        st.error("Let’s push for a stronger week ahead!")

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
        data = load_data(MEAL_FILE)
        data.append(meal_entry)
        save_data(MEAL_FILE, data)
        st.success("🍏 Meals saved! Here's your feedback:")

        all_meals = " ".join([breakfast, snack, lunch, dinner]).lower()
        if "candy" in all_meals or "soda" in all_meals:
            st.warning("🍬 Reduce sugary snacks and try healthier swaps like fruit or yogurt.")
        elif any(food in all_meals for food in ["fruit", "vegetable", "chicken", "egg", "fish"]):
            st.success("✅ Great nutrition choices! Balanced meals fuel results.")
        else:
            st.info("🥗 Add more whole foods, protein, and fiber. Avoid processed snacks.")

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
        data = load_data(BODY_STATS_FILE)
        data.append(entry)
        save_data(BODY_STATS_FILE, data)
        st.success("📊 Stats saved! Track weekly for progress.")

def ai_suggestions():
    st.subheader("🤖 AI Suggestions")
    st.markdown("- Add mobility stretches if you're sore.\n- Swap sugary drinks for lemon water.\n- End workouts with 5 minutes of deep breathing.")

def motivation_corner():
    st.subheader("🔥 Motivation Corner")
    st.markdown("> _\"You don't have to be extreme, just consistent.\"_ 💡\n> _\"Small steps lead to big changes.\"_ 🚶")

# Sidebar options
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


