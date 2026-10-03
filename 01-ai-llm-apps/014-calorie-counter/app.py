import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Calorie Counter", page_icon="🍽️", layout="centered")
st.title("🍽️ AI Calorie Counter")
st.markdown("Estimate calories & get healthier alternatives")

# Sidebar for API key
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password", value=os.environ.get("GEMINI_API_KEY", ""))
    st.markdown("---")
    st.markdown("Get your API key at [Google AI Studio](https://aistudio.google.com/)")

if not api_key:
    st.warning("Please enter your Gemini API key in the sidebar")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Main UI
st.subheader("🥗 Describe Your Meal")
meal_description = st.text_area("Meal Description", placeholder="e.g., 2 slices of pepperoni pizza, 1 cup of rice, grilled chicken salad with ranch dressing", height=100)

dietary_preference = st.selectbox("🥬 Dietary Preference", ["No Preference", "Vegetarian", "Vegan", "Keto", "Low-Carb", "Gluten-Free"])
goal = st.selectbox("🎯 Health Goal", ["Maintain Weight", "Lose Weight", "Build Muscle", "Gain Weight"])

if st.button("🔍 Analyze Meal", type="primary") and meal_description:
    with st.spinner("Analyzing your meal..."):
        prompt = f"""Analyze this meal and provide nutritional information:

Meal: {meal_description}
Dietary Preference: {dietary_preference}
Health Goal: {goal}

Provide:
1. **Estimated Calories**: Total calorie count
2. **Macronutrient Breakdown**: Protein, Carbs, Fat (in grams)
3. **Nutrition Rating**: Quick assessment (Excellent/Good/Fair/Poor)
4. **Healthier Alternatives**: 2-3 lower calorie options with comparison
5. **Tips**: Quick tips for making it healthier

Format nicely with emojis and sections."""

        try:
            response = model.generate_content(prompt)
            st.success("Meal Analysis Complete!")
            st.markdown(response.text)
            st.info("💡 Note: These are estimates. For exact values, use a nutrition database.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Quick add section
st.markdown("---")
st.subheader("⚡ Quick Add Common Foods")
quick_foods = st.multiselect("Select foods to add:", [
    "Apple (1 medium)", "Banana (1 medium)", "Chicken Breast (100g)",
    "White Rice (1 cup)", "Brown Rice (1 cup)", "Egg (1 large)",
    "Milk (1 cup)", "Greek Yogurt (1 cup)", "Almonds (30g)",
    "Avocado (1/2)", "Salmon (100g)", "Pasta (1 cup)"
])

if quick_foods:
    st.write("Selected:", ", ".join(quick_foods))

st.markdown("---")
st.caption("Built with Streamlit & Gemini AI | Not medical advice")
