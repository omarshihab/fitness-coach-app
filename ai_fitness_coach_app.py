import streamlit as st
import random

# Initialize session state
if "username" not in st.session_state:
    st.session_state.username = ""

if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# Login system
def login():
    st.sidebar.title("👤 Login")
    username = st.sidebar.text_input("Enter your username")
    if username:
        st.session_state.username = username
        if username not in st.session_state.user_data:
            st.session_state.user_data[username] = {}
        st.sidebar.success(f"Welcome, {username}!")

login()

# Stop until login
if not st.session_state.username:
    st.stop()

username = st.session_state.username

# AI Suggestions
def ai_suggestions():
    st.subheader("🧠 AI Suggestions")
    tips = [
        "🏃 Add 10 extra minutes to your cardio this week.",
        "💪 Try supersetting your biceps and triceps exercises.",
        "🥦 Include more leafy greens for extra fiber.",
        "🛌 Aim for at least 8 hours of sleep to recover better.",
        "🚶 Walk for 10 mins after meals to improve digestion."
    ]
    st.info(random.choice(tips))

# Motivation Corner
def motivation_corner():
    st.subheader("🌟 Motivation Corner")
    quotes = [
        "✨ Consistency beats motivation.",
        "🔥 You're stronger than you think.",
        "💥 Every rep counts.",
        "🙌 Show up for yourself every day.",
        "🚀 Great things take time."
    ]
    st.success(random.choice(quotes))

# Meal Log & Feedback
def meal_feedback():
    st.subheader("🍽️ Daily Meal Log & Feedback")
    breakfast = st.text_input("🍳 What did you have for breakfast?")
    snack = st.text_input("🍌 What did you snack on?")
    lunch = st.text_input("🥗 What did you have for lunch?")
    dinner = st.text_input("🍝 What did you have for dinner?")

    if st.button("Submit Meals"):
        full_day = f"{breakfast} {snack} {lunch} {dinner}".lower()
        feedback = []

        if "chips" in full_day or "soda" in full_day:
            feedback.append("⚠️ Try to reduce processed snacks and sugary drinks.")
        if "salad" in full_day or "vegetables" in full_day:
            feedback.append("✅ Great job including veggies!")
        if "chicken" in full_day or "fish" in full_day:
            feedback.append("🍗 Nice source of protein!")
        if "fruit" in full_day:
            feedback.append("🍎 Good job adding fruits!")
        if not feedback:
            feedback.append("👍 Keep it up! Try to mix lean protein, veggies, and whole grains.")

        for f in feedback:
            st.write(f)

# Body Stats & Goals
def body_stats_and_goals():
    st.subheader("📏 Body Stats & Goals")
    height = st.number_input("📐 Height (cm)", min_value=100, max_value=250)
    weight = st.number_input("⚖️ Weight (kg)", min_value=20, max_value=200)
    goal = st.selectbox("🎯 Your Goal", ["Lose Weight", "Build Muscle", "Improve Stamina", "Stay Healthy"])

    if st.button("Save Stats"):
        st.session_state.user_data[username]["height"] = height
        st.session_state.user_data[username]["weight"] = weight
        st.session_state.user_data[username]["goal"] = goal
        st.success("✅ Stats saved!")

# Weekly Workout Plan
def show_weekly_plan():
    st.subheader("📅 Weekly Workout Plan")
    user_data = st.session_state.user_data[username]
    weekly_plan = user_data.get("weekly_plan", {})

    if not weekly_plan:
        st.info("You haven't added any plans yet.")
    else:
        for day, plan in weekly_plan.items():
            st.markdown(f"**{day}**: {plan}")

    with st.form("weekly_plan_form"):
        day = st.selectbox("📆 Select a day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        plan = st.text_area("✍️ Describe your workout:")
        submitted = st.form_submit_button("Save Plan")
        if submitted:
            if "weekly_plan" not in user_data:
                user_data["weekly_plan"] = {}
            user_data["weekly_plan"][day] = plan
            st.success(f"✅ Plan for {day} saved!")

# Progress Tracker
def progress_tracker():
    st.subheader("📈 Progress Tracker")
    weight_change = st.number_input("📊 Change in weight (kg)", step=0.1)
    mood = st.selectbox("😊 How do you feel this week?", ["Great", "Okay", "Tired", "Motivated"])
    notes = st.text_area("📝 Any reflections or notes?")

    if st.button("Save Progress"):
        if "progress" not in st.session_state.user_data[username]:
            st.session_state.user_data[username]["progress"] = []
        st.session_state.user_data[username]["progress"].append({
            "weight_change": weight_change,
            "mood": mood,
            "notes": notes
        })
        st.success("📍 Progress saved!")

# Workout Log
def workout_log():
    st.subheader("🏋️ Workout Log")
    workout = st.text_input("🧾 What workout did you do today?")
    duration = st.number_input("⏱️ Duration (minutes)", step=1)

    if st.button("Log Workout"):
        if "workouts" not in st.session_state.user_data[username]:
            st.session_state.user_data[username]["workouts"] = []
        st.session_state.user_data[username]["workouts"].append({
            "workout": workout,
            "duration": duration
        })
        st.success("✅ Workout logged!")

# Notes & Journal
def notes_journal():
    st.subheader("📓 Notes & Journal")
    entry = st.text_area("🧠 Write anything you want to reflect on:")
    if st.button("Save Note"):
        if "journal" not in st.session_state.user_data[username]:
            st.session_state.user_data[username]["journal"] = []
        st.session_state.user_data[username]["journal"].append(entry)
        st.success("📝 Note saved!")

# Hydration Log
def hydration_log():
    st.subheader("💧 Hydration Tracker")
    water = st.number_input("How much water did you drink today? (in liters)", step=0.1)
    if st.button("Log Water Intake"):
        if "hydration" not in st.session_state.user_data[username]:
            st.session_state.user_data[username]["hydration"] = []
        st.session_state.user_data[username]["hydration"].append(water)
        st.success("🥤 Hydration logged!")

# NEW: AI 4-Day Workout Generator (Static Example)
def ai_4day_workout():
    st.subheader("💪 AI 4-Day Workout Generator")
    goal = st.selectbox("🎯 Goal", ["Lose Weight", "Build Muscle", "Improve Stamina", "Stay Healthy"])
    if st.button("Generate Plan"):
        plan = {
            "Day 1": "Upper Body Strength – Bench Press 4x8, Pull-ups 4x6, Shoulder Press 3x10, Bicep Curls 3x12",
            "Day 2": "Lower Body Strength – Squats 4x8, Lunges 3x12, Leg Press 3x10, Calf Raises 4x15",
            "Day 3": "Push & Core – Push-ups 4x15, Dips 3x12, Plank 3x60s, Russian Twists 3x20",
            "Day 4": "Pull & Cardio – Deadlifts 4x6, Bent Rows 3x10, Lat Pulldown 3x12, 20 min HIIT Cardio"
        }
        for day, routine in plan.items():
            st.write(f"**{day}**: {routine}")

# UI – Dropdowns in sidebar
st.title("🏋️ AI Fitness Coach App")

with st.sidebar:
    section = st.selectbox("📂 Navigate", [
        "🧠 AI Suggestions",
        "🌟 Motivation Corner",
        "🍽️ Meal Log & Feedback",
        "📏 Body Stats & Goals",
        "📅 Weekly Workout Plan",
        "📈 Progress Tracker",
        "🏋️ Workout Log",
        "📓 Notes & Journal",
        "💧 Hydration Log",
        "💪 AI 4-Day Workout Generator"  # NEW SECTION
    ])

# Route user to the selected section
if section == "🧠 AI Suggestions":
    ai_suggestions()
elif section == "🌟 Motivation Corner":
    motivation_corner()
elif section == "🍽️ Meal Log & Feedback":
    meal_feedback()
elif section == "📏 Body Stats & Goals":
    body_stats_and_goals()
elif section == "📅 Weekly Workout Plan":
    show_weekly_plan()
elif section == "📈 Progress Tracker":
    progress_tracker()
elif section == "🏋️ Workout Log":
    workout_log()
elif section == "📓 Notes & Journal":
    notes_journal()
elif section == "💧 Hydration Log":
    hydration_log()
elif section == "💪 AI 4-Day Workout Generator":
    ai_4day_workout()




