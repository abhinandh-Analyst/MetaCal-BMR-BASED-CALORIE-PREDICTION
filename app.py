import streamlit as st
import pandas as pd
import joblib
import base64

# --- Load trained model ---
calorie_model = joblib.load("best_model.pkl")

# --- Function to convert image to base64 ---
def get_base64_image(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- Load background image (must be in same folder as this file) ---
img_base64 = get_base64_image("flat-lay-sport-frame-with-salad_23-2148531521.jpg")

# --- Page Style with background image ---
page_bg = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
h1 {{
    color:red;
    text-align: center;
    font-family: 'Helvetica', sans-serif;
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- App Title ---
st.markdown(
    "<h1 style='color: black; text-align: center; font-family: Helvetica;'>🍽️ MetaCal - Calorie Intake Prediction</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Change the background color of select boxes */
    div[data-baseweb="select"] > div > div {
        background-color: black !important;
    }

    /* Change text color and background of number/text inputs */
    input {
        color: white!important;       /* Text color inside input */
        background-color: black!important; /* Input background */
    }

    /* Change the label color (Age, Gender, etc.) */
    label {
        color: black!important;
        font-weight: bold!important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --- User Inputs ---
gender = st.selectbox("Gender", ["Male", "Female"])
gender_value = 0 if gender == "Male" else 1

age = st.number_input("Age", min_value=15, max_value=75, value=25, help="[15–75] Age of the subject in years.")
meal = st.number_input("Daily Meal Frequency", min_value=2, max_value=4, value=3, help="[2–4] Number of daily meals consumed on average.")
exercise = st.number_input("Physical Exercise (0=None → 4=Extremely heavy)", min_value=0, max_value=4, value=1, help="[0–4] Amount of daily exercise (0=None, 4=Heavy).")
height = st.number_input("Height (cm)", min_value=122, max_value=188, value=170, help="[122–188] Height of the subject in cm.")
weight = st.number_input("Weight (kg)", min_value=35, max_value=150, value=65, help="[35–150] Weight of the subject in kg.")

# --- BMR Calculation ---
if gender == "Male":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

# st.info(f"Calculated BMR: {bmr:.2f} kcal/day")
# --- Display BMR with custom color ---
st.markdown(
    f"""
   <div style="
                background-color: #004d00;
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 20px;
                display: inline-block;
                border: 2px solid #002600;
    ">
        Calculated BMR: {bmr:.2f} kcal/day
    </div>
    """,
    unsafe_allow_html=True
)



carbs = st.number_input("Carbs (g)", min_value=129, max_value=461, value=250, help="[129–461] Total carbohydrate intake per day (g).")
proteins = st.number_input("Proteins (g)", min_value=51, max_value=684, value=80, help="[51–184] Total protein intake per day (g).")

# --- Prepare input data ---
input_data = pd.DataFrame({
    "Gender": [gender_value],
    "Age": [age],
    "Daily Meal Frequency": [meal],
    "Physical Exercise": [exercise],
    "Height": [height],
    "Weight": [weight],
    "BMR": [bmr],
    "Carbs": [carbs],
    "Proteins": [proteins]
})

# --- Predict Calories ---
if st.button("Predict Calories"):
    try:
        prediction = calorie_model.predict(input_data)
        st.markdown(
            f"""
            <div style="
                background-color: #004d00;
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 20px;
                display: inline-block;
                border: 2px solid #002600;
            ">
                Predicted Daily Calorie Intake: {prediction[0]:.0f} kcal
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Prediction error: {e}")



