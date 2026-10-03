"""
SQL Generator - Natural Language to SQL Query
Convert plain English to SQL queries using Gemini
"""

import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(
    page_title="SQL Generator",
    page_icon="🗄️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .sql-box {background-color: #1a2332; padding: 1rem; border-radius: 0.5rem; font-family: monospace;}
    .success-box {background-color: #0d3320; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #28a745;}
</style>
""", unsafe_allow_html=True)

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except:
        return os.environ.get("GEMINI_API_KEY", "")

def init_gemini(api_key):
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def generate_sql(model, natural_language, db_type):
    """Generate SQL from natural language"""
    prompt = f"""Convert this request into a SQL query for {db_type}.

Request: {natural_language}

Rules:
- Return ONLY the SQL query (no explanations)
- Use standard SQL syntax for {db_type}
- If the request is ambiguous, make reasonable assumptions
- Wrap table/column names in backticks if needed
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def explain_sql(model, sql):
    """Explain what a SQL query does"""
    prompt = f"""Explain this SQL query in simple terms:

{sql}

Provide a brief explanation of what it does."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("🗄️ SQL Generator")
    st.caption("Convert Natural Language to SQL Queries")

    with st.sidebar:
        st.header("⚙️ Settings")
        api_key = get_api_key()

        if not api_key:
            st.warning("Enter your Gemini API key")
            api_key = st.text_input("Gemini API Key", type="password")
            if api_key:
                st.session_state.api_key = api_key
                st.rerun()
        else:
            st.success("API Key loaded")

        st.markdown("---")
        st.markdown("### Supported Databases")
        st.markdown("- PostgreSQL")
        st.markdown("- MySQL")
        st.markdown("- SQLite")
        st.markdown("- SQL Server")

    if "api_key" not in st.session_state and api_key:
        st.session_state.api_key = api_key

    if not st.session_state.get("api_key"):
        st.error("Please enter your Gemini API key in the sidebar.")
        return

    if not init_gemini(st.session_state.api_key):
        st.error("Failed to initialize Gemini.")
        return

    model = genai.GenerativeModel('gemini-1.5-flash')

    # Database selection
    db_type = st.selectbox(
        "📊 Select Database",
        ["PostgreSQL", "MySQL", "SQLite", "SQL Server"],
        help="The SQL dialect to generate"
    )

    # Input
    st.subheader("💬 Describe Your Query")
    natural_language = st.text_area(
        "What do you want to find?",
        placeholder="Example: Find all users who signed up in the last 30 days and have made at least one purchase",
        height=100
    )

    col1, col2 = st.columns(2)
    with col1:
        generate = st.button("🔄 Generate SQL", type="primary", use_container_width=True)
    with col2:
        clear = st.button("🗑️ Clear", use_container_width=True)

    if clear:
        st.session_state.generated_sql = ""
        st.session_state.explanation = ""
        st.rerun()

    if generate and natural_language:
        with st.spinner("Generating SQL..."):
            sql = generate_sql(model, natural_language, db_type)
            st.session_state.generated_sql = sql

            if not sql.startswith("Error"):
                explanation = explain_sql(model, sql)
                st.session_state.explanation = explanation

    # Display results
    if st.session_state.get("generated_sql"):
        st.markdown("---")
        st.subheader("📝 Generated SQL")
        st.code(st.session_state.generated_sql, language="sql")

        # Copy button
        st.button("📋 Copy to Clipboard", key="copy_btn")

        if st.session_state.get("explanation"):
            st.markdown("---")
            st.subheader("💡 Explanation")
            st.markdown(st.session_state.explanation)

    # Example prompts
    st.markdown("---")
    st.subheader("📝 Example Prompts")
    examples = [
        "Show all orders with total over $100",
        "Count users by their registration month",
        "Find products with low inventory (< 10 units)",
        "Get the top 5 customers by total purchases"
    ]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex}"):
            st.session_state.example = ex
            st.rerun()

if __name__ == "__main__":
    main()
