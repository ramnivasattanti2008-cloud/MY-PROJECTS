import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sqlite3

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

DB_PATH = "expenses.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()


def add_expense(date, amount, category, description):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO expenses (date, amount, category, description) VALUES (?, ?, ?, ?)',
              (date, amount, category, description))
    conn.commit()
    conn.close()


def get_expenses():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query('SELECT * FROM expenses ORDER BY date DESC', conn)
    conn.close()
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
    return df


def delete_expense(expense_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()


def get_monthly_totals():
    df = get_expenses()
    if df.empty:
        return pd.DataFrame()
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month')['amount'].sum().reset_index()
    monthly['month'] = monthly['month'].astype(str)
    return monthly


def get_category_totals():
    df = get_expenses()
    if df.empty:
        return pd.DataFrame()
    return df.groupby('category')['amount'].sum().reset_index()


init_db()

st.title("Expense Tracker")
st.markdown("Track your expenses and visualize spending patterns")

if 'show_form' not in st.session_state:
    st.session_state.show_form = False

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Add Expense")

    with st.form("expense_form", clear_on_submit=True):
        date = st.date_input("Date", datetime.now())
        amount = st.number_input("Amount (₹)", min_value=0.01, step=0.01, format="%.2f")

        categories = [
            'Food & Dining',
            'Transportation',
            'Shopping',
            'Entertainment',
            'Bills & Utilities',
            'Healthcare',
            'Education',
            'Travel',
            'Groceries',
            'Personal Care',
            'Other'
        ]
        category = st.selectbox("Category", categories)
        description = st.text_input("Description (optional)")

        submitted = st.form_submit_button("Add Expense", use_container_width=True)

        if submitted and amount > 0:
            add_expense(date.strftime('%Y-%m-%d'), amount, category, description)
            st.success("Expense added successfully!")
            st.rerun()

with col2:
    tab1, tab2, tab3 = st.tabs(["Overview", "Monthly Trend", "By Category"])

    df = get_expenses()

    with tab1:
        st.subheader("Recent Expenses")

        if df.empty:
            st.info("No expenses recorded yet. Add your first expense!")
        else:
            col_a, col_b, col_c = st.columns(3)

            total = df['amount'].sum()
            col_a.metric("Total Expenses", f"₹{total:,.2f}")
            col_b.metric("Number of Expenses", len(df))
            col_c.metric("Average Expense", f"₹{total/len(df):,.2f}")

            st.divider()

            display_df = df.copy()
            display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
            display_df['amount'] = display_df['amount'].apply(lambda x: f"₹{x:,.2f}")

            for idx, row in df.sort_values('date', ascending=False).head(10).iterrows():
                with st.container():
                    cols = st.columns([1, 3, 1, 1])
                    cols[0].write(f"📅 {row['date'].strftime('%b %d')}")
                    cols[1].write(f"**{row['category']}**")
                    if row['description']:
                        cols[1].caption(row['description'])
                    cols[2].write(f"₹{row['amount']:,.2f}")
                    if cols[3].button("Delete", key=f"del_{row['id']}"):
                        delete_expense(row['id'])
                        st.rerun()

    with tab2:
        st.subheader("Monthly Spending Trend")

        monthly = get_monthly_totals()

        if monthly.empty:
            st.info("No data to display. Add some expenses to see trends.")
        else:
            fig = px.bar(
                monthly,
                x='month',
                y='amount',
                color='amount',
                color_continuous_scale='Reds',
                title="Monthly Expenses"
            )
            fig.update_layout(
                xaxis_title="Month",
                yaxis_title="Amount (₹)",
                showlegend=False,
                xaxis=dict(tickangle=-45)
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Cumulative Spending")
            monthly['cumulative'] = monthly['amount'].cumsum()
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=monthly['month'],
                y=monthly['cumulative'],
                mode='lines+markers',
                fill='tozeroy',
                line=dict(color='#e94560', width=3)
            ))
            fig2.update_layout(
                xaxis_title="Month",
                yaxis_title="Cumulative Amount (₹)",
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.subheader("Expenses by Category")

        cat_df = get_category_totals()

        if cat_df.empty:
            st.info("No data to display. Add some expenses to see category breakdown.")
        else:
            col_left, col_right = st.columns(2)

            with col_left:
                fig_pie = px.pie(
                    cat_df,
                    values='amount',
                    names='category',
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_layout(title="Category Distribution")
                st.plotly_chart(fig_pie, use_container_width=True)

            with col_right:
                fig_bar = px.bar(
                    cat_df.sort_values('amount', ascending=True),
                    x='amount',
                    y='category',
                    orientation='h',
                    color='amount',
                    color_continuous_scale='Reds'
                )
                fig_bar.update_layout(
                    title="Category Breakdown",
                    xaxis_title="Amount (₹)",
                    yaxis_title="Category",
                    showlegend=False
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            st.divider()
            st.subheader("Category Details")

            for _, row in cat_df.sort_values('amount', ascending=False).iterrows():
                percentage = (row['amount'] / cat_df['amount'].sum()) * 100
                progress = percentage / 100
                st.write(f"**{row['category']}**: ₹{row['amount']:,.2f} ({percentage:.1f}%)")
                st.progress(progress, text="")

st.divider()
st.caption("Expense Tracker - Built with Streamlit")
