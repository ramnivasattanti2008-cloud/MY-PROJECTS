import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="SQL Query Builder", page_icon="🗃️", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .sql-box { background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; font-family: 'Courier New', monospace; }
</style>
""", unsafe_allow_html=True)

st.title("🗃️ SQL Query Builder AI")
st.caption("Describe what data you want in plain English, get SQL instantly")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password",
                           value=os.environ.get("GEMINI_API_KEY", ""))
    st.caption("Get your key at [Google AI Studio](https://aistudio.google.com/)")

    st.divider()
    st.subheader("📊 Database Type")
    db_type = st.selectbox("Target Database", ["PostgreSQL", "MySQL", "SQLite", "SQL Server", "Oracle"])

    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key")

# Main content
st.markdown("### 📝 Describe Your Data Need")
description = st.text_area(
    "What data do you want?",
    height=120,
    placeholder="Example: Show all customers who ordered more than $500 in the last month, sorted by total amount"
)

col1, col2 = st.columns(2)
with col1:
    st.markdown("**📋 Tables Available** (optional)")
    tables = st.text_input("Table names", placeholder="customers, orders, products")
with col2:
    st.markdown("**🔗 Relationships** (optional)")
    joins = st.text_input("Relationships", placeholder="customers.id = orders.customer_id")

if st.button("⚡ Generate SQL", type="primary", disabled=not api_key):
    if not description.strip():
        st.error("❌ Please describe what data you need")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            context = f"""Database type: {db_type}"""
            if tables:
                context += f"\nTables: {tables}"
            if joins:
                context += f"\nRelationships: {joins}"

            prompt = f"""Generate a SQL query based on this natural language description.

{context}

Description: {description}

Rules:
- Use proper JOIN syntax for {db_type}
- Include appropriate WHERE clauses
- Add ORDER BY if sorting makes sense
- Use aliases for readability
- Add comments explaining complex parts

Return ONLY the SQL query, no markdown code blocks or explanation."""

            with st.spinner("🔨 Building query..."):
                response = model.generate_content(prompt)

            st.success("✅ Query Generated!")

            # Display SQL
            sql_query = response.text.strip()
            if sql_query.startswith("```"):
                sql_query = sql_query.split("```")[1]
                if sql_query.startswith("sql"):
                    sql_query = sql_query[3:]

            st.markdown("### 📄 Generated SQL")
            st.markdown(f"""
            <div class="sql-box">
            <code>{sql_query}</code>
            </div>
            """, unsafe_allow_html=True)

            # Copy button
            st.code(sql_query, language="sql")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider()
st.caption("💡 Tip: Mention aggregations (SUM, COUNT), filters, and sorting for better results!")
