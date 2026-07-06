import streamlit as st
import numpy as np
import joblib
import os

MODEL_PATH = "Model.pkl"  # 👈 isi folder mein Model.pkl hona chahiye

# -----------------------------
# Load trained model
# -----------------------------
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"❌ File nahi mili: {os.path.abspath(MODEL_PATH)}")
        st.stop()
    try:
        return joblib.load(MODEL_PATH)
    except Exception as e:
        st.error(f"❌ Model load nahi ho paya: {e}")
        st.stop()

model = load_model()

st.set_page_config(page_title="Daily Calorie Requirement Predictor", page_icon="🔥")
st.title("🔥 Daily Calorie Requirement Predictor")
st.write("Apni details bharo aur apni daily calorie requirement jaano.")

# -----------------------------
# Input fields
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age (years)", min_value=1, max_value=100, value=25)
    gender = st.selectbox("Gender", ["Female", "Male"])
    height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
    weight_kg = st.number_input("Weight (kg)", min_value=20.0, max_value=250.0, value=70.0)
    sleep_hours = st.number_input("Sleep Hours", min_value=0.0, max_value=24.0, value=7.0)

with col2:
    activity_level = st.selectbox(
        "Activity Level",
        ["Extra Active", "Lightly Active", "Moderately Active", "Sedentary", "Very Active"]
    )
    water_intake_l = st.number_input("Water Intake (Liters)", min_value=0.0, max_value=10.0, value=2.5)
    goal = st.selectbox("Goal", ["Maintain Weight", "Weight Gain", "Weight Loss"])
    diet_type = st.selectbox("Diet Type", ["Eggetarian", "Non-Vegetarian", "Vegan", "Vegetarian"])

# -----------------------------
# Encoding maps
# NOTE: Ye alphabetical order (sklearn LabelEncoder ka default tareeka) follow karta hai.
# Agar aapki training mein encoding order alag tha (jaise apne khud numbers assign kiye the),
# to neeche wale maps ko apne training code ke hisaab se badal do.
# -----------------------------
gender_map = {"Female": 0, "Male": 1}

activity_map = {
    "Extra Active": 0,
    "Lightly Active": 1,
    "Moderately Active": 2,
    "Sedentary": 3,
    "Very Active": 4
}

goal_map = {
    "Maintain Weight": 0,
    "Weight Gain": 1,
    "Weight Loss": 2
}

diet_map = {
    "Eggetarian": 0,
    "Non-Vegetarian": 1,
    "Vegan": 2,
    "Vegetarian": 3
}

# -----------------------------
# Predict button
# -----------------------------
if st.button("Calculate Calorie Requirement"):
    # Column order EXACTLY matches: Age, Gender, Height_cm, Weight_kg,
    # Activity_Level, Sleep_Hours, Water_Intake_L, Goal, Diet_Type
    features = np.array([[
        age,
        gender_map[gender],
        height_cm,
        weight_kg,
        activity_map[activity_level],
        sleep_hours,
        water_intake_l,
        goal_map[goal],
        diet_map[diet_type]
    ]])

    try:
        prediction = model.predict(features)[0]
        st.success(f"✅ Estimated Daily Calorie Requirement: **{prediction:.0f} kcal/day**")
    except Exception as e:
        st.error(f"Prediction mein error aaya: {e}")
        st.info("Check karo ki input order aapke model training ke feature order se match kar raha hai.")

st.markdown("---")
st.caption("Model: Model.pkl | Made with Streamlit")
