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

IMAGE_URL = "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=800&q=80"

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
        st.write(f"**{day}**: {plan} — Train with intensity, stay consistent, and listen to your body.")

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
        st.info("You're doing okay — aim for at least 4 sessions to see steady progress.")
    else:
        st.error("😴 Let’s get moving — even short workouts add up over time!")

def meal_log():
    st.subheader("🍽️ Meal Log & AI Feedback")
    st.image(IMAGE_URL, use_container_width=True)
    breakfast = st.text_input("What did you eat for Breakfast?")
    snack = st.text_input("What did you eat for your Snack?")
    lunch = st.text_input("What did you eat for Lunch?")
    dinner = st.text_input("What did you eat for Dinner?")
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

        if any(junk in all_meals for junk in ["candy", "soda", "chips", "fast food"]):
            st.warning("⚠️ Try to reduce processed or sugary foods. Aim for whole foods like fruits, veggies, lean proteins, and water.")
        elif any(healthy in all_meals for healthy in ["chicken", "broccoli", "salad", "oats", "eggs", "fruit", "vegetable"]):
            st.success("✅ Solid food choices! You're fueling your body the right way.")
        else:
            st.info("👀 Try to add more protein, natural carbs, and fiber into your meals for energy and recovery.")

def body_stats():
    st.subheader("📏 Body Stats & Goals")
    st.image(IMAGE_URL, use_container_width=True)
    weight = st.number_input("Current Weight (kg)", min_value=0.0, step=0.5)
    waist = st.number_input("Waist Measurement (cm)", min_value=0.0, step=0.5)
    goal = st.text_input("What's your current fitness goal? (e.g., build strength, get lean)")
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
        st.success("📊 Stats saved! Review them weekly and adjust as needed.")

def ai_motivation():
    st.subheader("🔥 AI Motivation Corner")
    st.image(IMAGE_URL, use_container_width=True)
    st.markdown("You're stronger than your excuses. Keep pushing. Consistency over perfection. The hardest step is showing up!")

def ai_suggestions():
    st.subheader("🤖 AI Suggestions for Improvement")
    st.image(IMAGE_URL, use_container_width=True)
    st.markdown("- Aim for at least 7 hours of sleep each night.\n- Mix cardio and strength for balanced fitness.\n- Stay hydrated — at least 2L of water daily.\n- Track your progress weekly.\n- Don’t skip warm-ups and cool-downs!")

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
        "AI Motivation Corner",
        "AI Suggestions for Improvement"
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
elif option == "AI Motivation Corner":
    ai_motivation()
elif option == "AI Suggestions for Improvement":
    ai_suggestions()
