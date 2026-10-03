import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Recipe Manager", page_icon="🍳", layout="wide")

# Dark theme CSS
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .recipe-card { background-color: #1e2530; padding: 20px; border-radius: 10px; margin: 10px 0; }
    .ingredient-tag { background-color: #264f78; padding: 5px 10px; border-radius: 15px; display: inline-block; margin: 3px; }
    h1, h2, h3 { color: #ffffff !important; }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stNumberInput > div > div > input {
        background-color: #1e2530; color: white; border: 1px solid #3d4654;
    }
</style>
""", unsafe_allow_html=True)

# Initialize DB
def init_db():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recipes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, ingredients TEXT,
                  instructions TEXT, cooking_time INTEGER, created_at TEXT)''')
    conn.commit()
    conn.close()

def get_recipes():
    conn = sqlite3.connect('recipes.db')
    df = pd.read_sql('SELECT * FROM recipes ORDER BY created_at DESC', conn)
    conn.close()
    return df

def add_recipe(name, ingredients, instructions, cooking_time):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('INSERT INTO recipes (name, ingredients, instructions, cooking_time, created_at) VALUES (?, ?, ?, ?, ?)',
              (name, ingredients, instructions, cooking_time, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def delete_recipe(recipe_id):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
    conn.commit()
    conn.close()

init_db()

# Header
st.title("🍳 Recipe Manager")
st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 Add Recipe", "🔍 Browse & Search", "📊 Statistics"])

with tab1:
    st.header("Add New Recipe")
    with st.form("recipe_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Recipe Name", placeholder="e.g., Butter Chicken")
            ingredients = st.text_area("Ingredients (one per line)", placeholder="500g chicken\n2 cups yogurt\nSpices...")
            cooking_time = st.number_input("Cooking Time (minutes)", min_value=1, max_value=480, value=30)
        with col2:
            instructions = st.text_area("Instructions", placeholder="1. Marinate chicken...\n2. Cook sauce...", height=200)
        submitted = st.form_submit_button("Add Recipe", use_container_width=True)
        if submitted and name:
            add_recipe(name, ingredients, instructions, cooking_time)
            st.success("Recipe added successfully!")

with tab2:
    st.header("Browse & Search Recipes")
    search = st.text_input("🔍 Search recipes...", placeholder="Search by name or ingredients...")
    recipes = get_recipes()

    if search:
        recipes = recipes[
            recipes['name'].str.contains(search, case=False, na=False) |
            recipes['ingredients'].str.contains(search, case=False, na=False)
        ]

    if recipes.empty:
        st.info("No recipes found. Add some recipes first!")
    else:
        for _, row in recipes.iterrows():
            with st.container():
                st.markdown(f"### {row['name']}")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Ingredients:** {row['ingredients'][:100]}..." if len(str(row['ingredients'])) > 100 else f"**Ingredients:** {row['ingredients']}")
                    st.markdown(f"**Instructions:** {row['instructions'][:150]}..." if len(str(row['instructions'])) > 150 else f"**Instructions:** {row['instructions']}")
                with col2:
                    st.metric("⏱️ Time", f"{row['cooking_time']} min")
                    if st.button("🗑️ Delete", key=f"del_{row['id']}"):
                        delete_recipe(row['id'])
                        st.rerun()
                st.markdown("---")

with tab3:
    st.header("Recipe Statistics")
    recipes = get_recipes()
    if not recipes.empty:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(recipes.sort_values('cooking_time'), x='name', y='cooking_time',
                        title="Cooking Time by Recipe", color='cooking_time',
                        color_continuous_scale='Viridis')
            fig.update_layout(plot_bgcolor='#1e2530', paper_bgcolor='#0e1117',
                            font_color='white', xaxis_title="Recipe", yaxis_title="Minutes")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig2 = px.pie(recipes, names='name', values='cooking_time',
                         title="Cooking Time Distribution")
            fig2.update_layout(plot_bgcolor='#1e2530', paper_bgcolor='#0e1117', font_color='white')
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Add some recipes to see statistics!")
