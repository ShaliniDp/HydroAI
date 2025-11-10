import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import calculate_hydration, generate_prompt, get_ai_response
from datetime import datetime

# Streamlit page setup
st.set_page_config(page_title="HydroAI – Personalized Hydration Reminder", page_icon="💧", layout="centered")
st.title("💧 HydroAI – Personalized Hydration Reminder System")
st.write("A hybrid **Machine Learning + Generative AI** solution for hydration reminders.")

# Mode selection
mode = st.radio("Choose Mode:", ["Manual Input", "Dataset Mode"])

# ===================== MANUAL INPUT MODE =====================
if mode == "Manual Input":
    st.subheader("📥 Enter Your Details")
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age (years)", min_value=10, max_value=90, value=25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        weight = st.number_input("Weight (kg)", min_value=30, max_value=150, value=65)

    with col2:
        water_intake = st.number_input("Water Intake Today (L)", min_value=0.5, max_value=5.0, step=0.1, value=1.5)
        activity = st.selectbox("Activity Level", ["Low", "Medium", "High"])
        climate = st.selectbox("Climate", ["Moderate", "Hot", "Cold"])

    if st.button("💡 Get Hydration Reminder"):
        # ✅ ML calculation
        hydration_target = calculate_hydration(weight, climate, activity)
        remaining = round(hydration_target - water_intake, 2)

        # ✅ AI Prompt
        prompt = generate_prompt(age, gender, weight, activity, water_intake, climate)
        ai_response = get_ai_response(prompt)

        # 🚦 Status Card
        st.subheader("🚦 Hydration Status")
        if remaining > 0:
            st.warning(f"⚠️ Slightly Underhydrated – You need {remaining} L more water today.")
        else:
            st.success("✅ Adequately Hydrated – You’ve reached your hydration goal!")

        # 🕒 AI Reminder Schedule
        st.subheader("📋 AI-Generated Reminder Schedule")
        st.write(ai_response)

        # 📊 Intake vs Target Chart
        st.subheader("📊 Intake vs Target")
        fig, ax = plt.subplots(figsize=(5,3))
        bars = ax.bar(["Your Intake", "Target"], [water_intake, hydration_target], color=["skyblue", "lightgreen"])
        ax.set_ylabel("Liters")
        ax.set_ylim(0, max(water_intake, hydration_target) + 1)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 0.1,
                    f"{bar.get_height():.2f} L", ha='center', color='black', fontsize=10)
        st.pyplot(fig)

# ===================== DATASET MODE =====================
elif mode == "Dataset Mode":
    st.subheader("📂 Process Dataset")

    DEFAULT_DATASET = "health_fitness_dataset_clean.csv"

    try:
        df = pd.read_csv(DEFAULT_DATASET)
        st.success(f"✅ Dataset loaded: {DEFAULT_DATASET}")
        st.write(df.head())

        if st.button("🚀 Generate Reminders for Dataset"):
            st.write("🔄 Processing all users...")

            results = []
            progress = st.progress(0)

            for index, row in df.iterrows():
                try:
                    age = row.get("age", "N/A")
                    gender = row.get("gender", "N/A")
                    weight = row.get("weight_kg", 0)
                    water_intake = row.get("hydration_level", 0)
                    activity = row.get("activity_type", "Medium")
                    climate = "Moderate"

                    # ML calculation
                    hydration_target = calculate_hydration(weight, climate, activity)
                    prompt = generate_prompt(age, gender, weight, activity, water_intake, climate)
                    ai_tip = get_ai_response(prompt)

                    results.append({
                        "Age": age,
                        "Gender": gender,
                        "Weight (kg)": weight,
                        "Water Intake (L)": water_intake,
                        "Target (L)": hydration_target,
                        "AI Reminder": ai_tip
                    })

                    progress.progress((index + 1) / len(df))

                except Exception as e:
                    results.append({"Error": f"❌ Error processing row {index+1}: {str(e)}"})

            # Show results
            result_df = pd.DataFrame(results)
            st.subheader("📊 Hydration Reminder Results")
            st.dataframe(result_df)

            # Download option
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Reminder Plan CSV",
                               data=csv,
                               file_name="hydration_reminder_plan.csv",
                               mime="text/csv")

    except FileNotFoundError:
        st.error("❌ Dataset file not found! Place 'wellness_dataset.csv' in the same folder.")
