import streamlit as st
from openai import OpenAI

# ------------------------
# HARD-CODED API KEY
# ⚠️ Do not share this!
# ------------------------
client = OpenAI(api_key="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")

st.title("AI Fitness Coach 🏋️")

st.write("Click the button to generate your 4-day workout plan.")

if st.button("Generate Plan"):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a fitness coach who creates structured workout plans."},
                {"role": "user", "content": "Make me a 4-day workout plan with 4 sets per exercise."}
            ],
            max_tokens=600
        )
        workout_plan = response.choices[0].message.content
        st.subheader("Here’s your plan:")
        st.write(workout_plan)
    except Exception as e:
        st.error(f"Error while generating plan: {e}")
