import streamlit as st 
import random 
from openai import OpenAI 

# ---------------------------
# HARD-CODE YOUR API KEY + PROJECT ID HERE
# ---------------------------
client = OpenAI(
    api_key="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",
    project="proj_ro5y6asevklX4a0Mxd7HWvRA"  # <-- paste your Project ID here
)

st.set_page_config(page_title="AI Fitness Coach App", layout="wide")

# ---------------------------
# Session State & Login
# ---------------------------
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

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

# ---------------------------
# App Title
# ---------------------------
st.title("🏋️ AI Fitness Coach App")

# ---------------------------
# Sections / Features
# ---------------------------
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

def notes_journal():
    st.subheader("📓 Notes & Journal")
    entry = st.text_area("🧠 Write anything you want to reflect on:")
    if st.button("Save Note"):
        if "journal" not in st.session_state.user_data[username]:
            st.session_state.user_data[username]["journal"] = []
        st.session_state.user_data[username]["journal"].append(entry)
        st.success("📝 Note saved!")

def hydration_log():
    st.subheader("💧 Hydration Tracker")
    water = st.number_input("How much water did you drink today? (in liters)", step=0.1)
    if st.button("Log Water Intake"):
        if "hydration" not in st.session_state.user_data[username]:
            st.session_state.user_data[username]["hydration"] = []
        st.session_state.user_data[username]["hydration"].append(water)
        st.success("🥤 Hydration logged!")

# ---------------------------
# AI 4-Day Workout Generator
# ---------------------------
def ai_4day_workout():
    st.subheader("💪 AI 4-Day Workout Generator")
    display_name = st.text_input("Your name (optional)", username)
    goal = st.selectbox("🎯 Goal", ["Lose Weight", "Build Muscle", "Improve Stamina", "Stay Healthy"])
    equipment = st.text_input("🏋️ Available equipment (comma separated)", "Dumbbells, Resistance Bands, Pull-Up Bar")
    level = st.selectbox("📚 Experience level", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Generate AI Plan"):
        prompt = f"""
        Create a clear, structured 4-day workout plan for {display_name or "the user"}.
        Goal: {goal}
        Experience level: {level}
        Available equipment: {equipment}
        Include these sections with headings exactly like this so I can parse them:
        Warm-up:
        Day 1:
        Day 2:
        Day 3:
        Day 4:
        Cool-down:
        """

        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional fitness trainer who writes concise, structured programs."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
            )
            workout_text = resp.choices[0].message.content

            st.session_state.user_data[username]["ai_4day_plan"] = workout_text

            # Parse into sections
            headings = ["Warm-up", "Day 1", "Day 2", "Day 3", "Day 4", "Cool-down"]
            sections = {h: [] for h in headings}
            current = None
            for line in workout_text.splitlines():
                stripped = line.strip()
                lower = stripped.lower()
                if lower.startswith("warm-up"): current = "Warm-up"; continue
                elif lower.startswith("day 1"): current = "Day 1"; continue
                elif lower.startswith("day 2"): current = "Day 2"; continue
                elif lower.startswith("day 3"): current = "Day 3"; continue
                elif lower.startswith("day 4"): current = "Day 4"; continue
                elif lower.startswith("cool-down"): current = "Cool-down"; continue
                if current:
                    sections[current].append(stripped)

            st.success("Here’s your AI-generated 4-day plan!")

            for h in headings:
                if sections[h]:
                    with st.expander(h, expanded=(h in ["Day 1"])):
                        st.write("\n".join(sections[h]))

            st.download_button(
                label="📥 Download Full Plan",
                data=workout_text,
                file_name=f"{(display_name or username)}_4_day_workout.txt"
            )
        except Exception as e:
            st.error(f"Error while generating plan: {e}")

# ---------------------------
# Sidebar Navigation
# ---------------------------
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
        "💪 AI 4-Day Workout Generator"
    ])

# ---------------------------
# Router
# ---------------------------
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
