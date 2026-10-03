import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Recipe Generator", page_icon="🍳", layout="centered")

# Dark theme styling
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .title { text-align: center; color: #f0f6fc; font-size: 2.5rem; margin-bottom: 0.5rem; }
    .subtitle { text-align: center; color: #8b949e; font-size: 1.1rem; margin-bottom: 2rem; }
    .recipe-box { background-color: #161b22; border-radius: 16px; padding: 25px; border: 1px solid #30363d; margin-top: 20px; }
    .recipe-header { color: #58a6ff; font-size: 1.5rem; border-bottom: 2px solid #238636; padding-bottom: 10px; margin-bottom: 20px; }
    .ingredient { background-color: #1c2128; padding: 8px 15px; border-radius: 20px; margin: 5px; display: inline-block; border: 1px solid #30363d; }
    .step { background-color: #1c2128; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #f0883e; }
    .step-number { background-color: #f0883e; color: #0e1117; width: 30px; height: 30px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 10px; }
    .tip-box { background: linear-gradient(135deg, #2d1f3d 0%, #1a1f2e 100%); border-radius: 12px; padding: 15px; border-left: 4px solid #a371f7; margin: 15px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">🍳 AI Recipe Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Turn ingredients into culinary magic</p>', unsafe_allow_html=True)

# Sidebar settings
with st.sidebar:
    st.header("🍽️ Settings")

    cuisine = st.selectbox("🌍 Cuisine", [
        "Italian", "Indian", "Mexican", "Chinese", "Japanese", "Thai",
        "French", "Mediterranean", "American", "Middle Eastern", "Any"
    ])

    difficulty = st.selectbox("📊 Difficulty", ["Easy", "Medium", "Hard", "Any"])

    meal_type = st.selectbox("🍴 Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert", "Any"])

    servings = st.slider("👥 Servings", 1, 8, 2)

    dietary = st.multiselect("🥗 Dietary", [
        "Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Keto", "Low-Carb"
    ])

    st.markdown("---")
    st.caption("Powered by Google Gemini")

# Main content
st.subheader("🥗 Your Ingredients")
st.caption("Enter ingredients you have, separated by commas")

ingredients = st.text_area(
    "Ingredients",
    placeholder="chicken, garlic, lemon, olive oil, rosemary...",
    height=100
)

dietary_text = ", ".join(dietary) if dietary else "None specified"

# Generate button
if st.button("🍳 Generate Recipe", use_container_width=True, type="primary"):
    if not ingredients:
        st.warning("Please enter at least one ingredient!")
    else:
        with st.spinner("👨‍🍳 Chef AI is cooking up something..."):
            try:
                api_key = os.environ.get("GEMINI_API_KEY", "")
                if api_key:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")

                    prompt = f"""Create an original, delicious recipe.

**Available Ingredients:** {ingredients}
**Cuisine:** {cuisine}
**Difficulty:** {difficulty}
**Meal Type:** {meal_type}
**Servings:** {servings}
**Dietary Restrictions:** {dietary_text}

Format your response EXACTLY like this:

---
RECIPE NAME: [Creative, appetizing name]

⏱️ PREP TIME: [X minutes]
⏱️ COOK TIME: [X minutes]
⏱️ TOTAL TIME: [X minutes]
🍽️ SERVINGS: {servings}
📊 DIFFICULTY: {difficulty}

🥗 INGREDIENTS:
[Numbered list of all ingredients with exact quantities]

👨‍🍳 INSTRUCTIONS:
[Numbered step-by-step instructions, clear and detailed]

💡 CHEF'S TIPS:
[2-3 helpful tips for best results]

🎨 SERVING SUGGESTION:
[How to plate and serve the dish]
---
"""
                    response = model.generate_content(prompt)
                    recipe = response.text
                else:
                    recipe = f"""⚠️ **Demo Mode** - Set `GEMINI_API_KEY` for real generation.

---
**Your Recipe Preview**

🥘 *Using ingredients: {ingredients}*

⏱️ Configure your Gemini API key to generate the complete recipe with instructions, timing, and tips!
---
"""

                # Display recipe
                st.markdown(f'<div class="recipe-box">{recipe}</div>', unsafe_allow_html=True)

                # Show ingredient tags
                ingredient_list = [i.strip() for i in ingredients.split(",") if i.strip()]
                st.markdown("### 🏷️ Ingredient Tags")
                tags_html = " ".join([f'<span class="ingredient">🍽️ {i}</span>' for i in ingredient_list])
                st.markdown(tags_html, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error generating recipe: {str(e)}")

# Recipe tips
st.markdown("---")
st.subheader("💡 Pro Tips")
tips_col1, tips_col2, tips_col3 = st.columns(3)

with tips_col1:
    st.markdown("""
    <div class="tip-box">
    <strong>🥕 Fresh is Best</strong><br>
    Use seasonal, fresh ingredients for the most flavorful results.
    </div>
    """, unsafe_allow_html=True)

with tips_col2:
    st.markdown("""
    <div class="tip-box">
    <strong>🔪 Prep First</strong><br>
    Chop, measure, and prepare all ingredients before cooking.
    </div>
    """, unsafe_allow_html=True)

with tips_col3:
    st.markdown("""
    <div class="tip-box">
    <strong>🌡️ Season to Taste</strong><br>
    Adjust seasoning at the end and taste as you go.
    </div>
    """, unsafe_allow_html=True)
