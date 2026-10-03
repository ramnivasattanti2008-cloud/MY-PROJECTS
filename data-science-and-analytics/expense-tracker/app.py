import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

st.set_page_config(page_title="ExpenseTracker", page_icon="💰", layout="wide")

DEFAULT_CATEGORIES = [
    "Food & Dining", "Transportation", "Shopping", "Entertainment",
    "Bills & Utilities", "Healthcare", "Travel", "Education",
    "Personal Care", "Gifts & Donations", "Investments", "Other"
]

if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Description", "Amount", "Category"])

def add_expense(date, description, amount, category):
    new_expense = pd.DataFrame([[date, description, amount, category]],
                                columns=["Date", "Description", "Amount", "Category"])
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

def delete_expense(index):
    st.session_state.expenses = st.session_state.expenses.drop(index).reset_index(drop=True)

def import_csv(file):
    try:
        df = pd.read_csv(file)
        required_cols = {"Date", "Description", "Amount", "Category"}
        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            return False, f"Missing columns: {', '.join(missing)}"

        df["Date"] = pd.to_datetime(df["Date"])
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df = df.dropna(subset=["Amount", "Date"])
        st.session_state.expenses = pd.concat([st.session_state.expenses, df], ignore_index=True)
        return True, f"Imported {len(df)} expenses"
    except Exception as e:
        return False, str(e)

def get_monthly_data(df):
    if df.empty:
        return pd.DataFrame()
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df.groupby("Month")["Amount"].sum().reset_index().sort_values("Month")

def get_category_data(df):
    if df.empty:
        return pd.DataFrame()
    return df.groupby("Category")["Amount"].sum().reset_index().sort_values("Amount", ascending=False)

st.title("💰 ExpenseTracker")
st.markdown("Track your spending, analyze patterns, and stay on budget")

# Sidebar for adding expenses
with st.sidebar:
    st.header("Add Expense")

    with st.form("expense_form", clear_on_submit=True):
        date = st.date_input("Date", datetime.today())
        description = st.text_input("Description", placeholder="What did you spend on?")
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
        category = st.selectbox("Category", DEFAULT_CATEGORIES)

        submitted = st.form_submit_button("Add Expense", use_container_width=True)

        if submitted and description and amount > 0:
            add_expense(date, description, amount, category)
            st.success("Expense added!")
            st.rerun()

    st.divider()

    # CSV Import
    st.header("Import Data")
    uploaded_file = st.file_uploader("Import CSV file", type=["csv"], label_visibility="collapsed")

    if uploaded_file:
        success, message = import_csv(uploaded_file)
        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)

    if not st.session_state.expenses.empty:
        st.divider()
        if st.button("Clear All Data", use_container_width=True):
            st.session_state.expenses = pd.DataFrame(columns=["Date", "Description", "Amount", "Category"])
            st.rerun()

# Main content area
if st.session_state.expenses.empty:
    st.info("👈 Add your first expense using the sidebar to get started!")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### How to Use

        1. **Add Expenses**: Use the sidebar form to record each expense
        2. **Categorize**: Assign expenses to categories for better tracking
        3. **Import CSV**: Upload existing data in CSV format

        ### CSV Format

        Your CSV should have these columns:
        ```
        Date,Description,Amount,Category
        2024-01-15,Groceries,85.50,Food & Dining
        2024-01-16,Gas,45.00,Transportation
        ```
        """)

    with col2:
        st.markdown("""
        ### Features

        - **Dashboard**: Overview of your spending
        - **Monthly Trends**: See spending over time
        - **Category Breakdown**: Pie and bar charts
        - **Recent Expenses**: Quick view of latest entries
        - **Export**: Download your data anytime

        ### Tips

        - Be consistent with categories for accurate reports
        - Review weekly to catch unexpected expenses
        - Set monthly budgets based on your analysis
        """)
else:
    # Summary cards
    df = st.session_state.expenses.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    total = df["Amount"].sum()
    this_month = df[df["Date"].dt.month == datetime.today().month]["Amount"].sum()
    avg_transaction = df["Amount"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Spent", f"${total:,.2f}")
    col2.metric("This Month", f"${this_month:,.2f}")
    col3.metric("Transactions", len(df))
    col4.metric("Avg Transaction", f"${avg_transaction:,.2f}")

    st.divider()

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Monthly Spending")
        monthly = get_monthly_data(df)
        if not monthly.empty:
            fig = px.bar(monthly, x="Month", y="Amount", color="Amount",
                         color_continuous_scale="Blues")
            fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Amount ($)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data for monthly chart")

    with col2:
        st.subheader("Category Breakdown")
        cat_data = get_category_data(df)
        if not cat_data.empty:
            fig = px.pie(cat_data, values="Amount", names="Category",
                         hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data for category chart")

    st.divider()

    # Recent transactions
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Recent Transactions")
        recent = df.sort_values("Date", ascending=False).head(10).copy()
        recent["Date"] = recent["Date"].dt.strftime("%b %d, %Y")
        recent["Amount"] = recent["Amount"].apply(lambda x: f"${x:,.2f}")

        display_cols = ["Date", "Description", "Category", "Amount"]
        st.dataframe(recent[display_cols], use_container_width=True, hide_index=True)

    with col2:
        st.subheader("Top Categories")
        top_cats = cat_data.head(5)
        for _, row in top_cats.iterrows():
            pct = (row["Amount"] / total) * 100
            st.markdown(f"**{row['Category']}**")
            st.progress(pct / 100, text=f"${row['Amount']:,.0f} ({pct:.1f}%)")

    st.divider()

    # All expenses with delete
    st.subheader("All Expenses")

    with st.expander("View and Manage All Expenses"):
        for i, row in df.sort_values("Date", ascending=False).iterrows():
            col1, col2, col3, col4, col5 = st.columns([2, 3, 2, 1, 0.5])
            with col1:
                st.text(row["Date"].strftime("%Y-%m-%d"))
            with col2:
                st.text(row["Description"][:40] + ("..." if len(row["Description"]) > 40 else ""))
            with col3:
                st.text(row["Category"])
            with col4:
                st.text(f"${row['Amount']:,.2f}")
            with col5:
                if st.button("🗑️", key=f"del_{i}"):
                    delete_expense(i)
                    st.rerun()
