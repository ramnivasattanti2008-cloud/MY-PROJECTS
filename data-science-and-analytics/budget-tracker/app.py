import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Budget Tracker", page_icon="💰", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .metric-card { background-color: #1e2530; padding: 15px; border-radius: 10px; text-align: center; }
    .income { color: #4ade80 !important; }
    .expense { color: #f87171 !important; }
    h1, h2, h3 { color: #ffffff !important; }
    .stSelectbox > div > div > div, .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: #1e2530; color: white; border: 1px solid #3d4654;
    }
    .stDateInput > div > div > input { background-color: #1e2530; color: white; }
</style>
""", unsafe_allow_html=True)

CATEGORIES = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Health", "Education", "Other"]

def init_db():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, amount REAL,
                  category TEXT, description TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS goals
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, target REAL, saved REAL)''')
    conn.commit()
    conn.close()

def get_transactions():
    conn = sqlite3.connect('budget.db')
    df = pd.read_sql('SELECT * FROM transactions ORDER BY date DESC', conn)
    conn.close()
    return df

def add_transaction(trans_type, amount, category, description, date):
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('INSERT INTO transactions (type, amount, category, description, date) VALUES (?, ?, ?, ?, ?)',
              (trans_type, amount, category, description, date))
    conn.commit()
    conn.close()

def delete_transaction(trans_id):
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('DELETE FROM transactions WHERE id = ?', (trans_id,))
    conn.commit()
    conn.close()

def get_goals():
    conn = sqlite3.connect('budget.db')
    df = pd.read_sql('SELECT * FROM goals', conn)
    conn.close()
    return df

def add_goal(name, target):
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('INSERT INTO goals (name, target, saved) VALUES (?, ?, 0)', (name, target))
    conn.commit()
    conn.close()

def update_goal_saved(goal_id, saved):
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('UPDATE goals SET saved = ? WHERE id = ?', (saved, goal_id))
    conn.commit()
    conn.close()

def delete_goal(goal_id):
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('DELETE FROM goals WHERE id = ?', (goal_id,))
    conn.commit()
    conn.close()

init_db()

st.title("💰 Personal Budget Tracker")
st.markdown("---")

# Summary cards
trans = get_transactions()
col1, col2, col3, col4 = st.columns(4)

income = trans[trans['type'] == 'Income']['amount'].sum() if not trans.empty else 0
expense = trans[trans['type'] == 'Expense']['amount'].sum() if not trans.empty else 0
balance = income - expense

with col1:
    st.markdown(f"<div class='metric-card'><h3>Total Income</h3><h2 style='color:#4ade80'>₹{income:,.2f}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h3>Total Expenses</h3><h2 style='color:#f87171'>₹{expense:,.2f}</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h3>Balance</h3><h2 style='color:#60a5fa'>₹{balance:,.2f}</h2></div>", unsafe_allow_html=True)
with col4:
    goals = get_goals()
    total_saved = goals['saved'].sum() if not goals.empty else 0
    st.markdown(f"<div class='metric-card'><h3>Savings</h3><h2 style='color:#fbbf24'>₹{total_saved:,.2f}</h2></div>", unsafe_allow_html=True)

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💵 Add Transaction", "📋 Transactions", "📊 Charts", "🎯 Savings Goals"])

with tab1:
    st.header("Add Transaction")
    with st.form("trans_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            trans_type = st.selectbox("Type", ["Income", "Expense"])
            amount = st.number_input("Amount (₹)", min_value=0.01, value=100.0, step=10.0)
            category = st.selectbox("Category", CATEGORIES if trans_type == "Expense" else ["Salary", "Freelance", "Investment", "Gift", "Other"])
        with col2:
            description = st.text_input("Description")
            date = st.date_input("Date", value=datetime.now())
        if st.form_submit_button("Add Transaction", use_container_width=True):
            add_transaction(trans_type, amount, category, description, date.isoformat())
            st.success("Transaction added!")

with tab2:
    st.header("All Transactions")
    trans = get_transactions()
    if not trans.empty:
        trans['date'] = pd.to_datetime(trans['date'])
        for _, row in trans.iterrows():
            col1, col2, col3 = st.columns([1, 4, 1])
            color = "#4ade80" if row['type'] == 'Income' else "#f87171"
            sign = "+" if row['type'] == 'Income' else "-"
            with col1:
                st.markdown(f"<h4 style='color:{color}'>{sign}₹{row['amount']:,.0f}</h4>")
            with col2:
                st.markdown(f"**{row['category']}** - {row['description']}<br><small>{row['date'].strftime('%Y-%m-%d')}</small>")
            with col3:
                if st.button("🗑️", key=f"del_{row['id']}"):
                    delete_transaction(row['id'])
                    st.rerun()
            st.markdown("---")
    else:
        st.info("No transactions yet. Add your first transaction!")

with tab3:
    st.header("Budget Analytics")
    trans = get_transactions()
    if not trans.empty:
        trans['date'] = pd.to_datetime(trans['date'])
        trans['month'] = trans['date'].dt.to_period('M')

        col1, col2 = st.columns(2)
        with col1:
            monthly = trans.groupby(['month', 'type'])['amount'].sum().reset_index()
            monthly['month'] = monthly['month'].astype(str)
            fig = px.bar(monthly, x='month', y='amount', color='type', barmode='group',
                        title="Monthly Income vs Expenses", color_discrete_map={'Income': '#4ade80', 'Expense': '#f87171'})
            fig.update_layout(plot_bgcolor='#1e2530', paper_bgcolor='#0e1117', font_color='white')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            expense_data = trans[trans['type'] == 'Expense']
            if not expense_data.empty:
                cat_totals = expense_data.groupby('category')['amount'].sum().reset_index()
                fig2 = px.pie(cat_totals, names='category', values='amount', title="Expenses by Category")
                fig2.update_layout(plot_bgcolor='#1e2530', paper_bgcolor='#0e1117', font_color='white')
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Add transactions to see charts!")

with tab4:
    st.header("Savings Goals")
    with st.form("goal_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            goal_name = st.text_input("Goal Name", placeholder="e.g., Emergency Fund")
        with col2:
            goal_target = st.number_input("Target Amount (₹)", min_value=100, value=10000, step=500)
        if st.form_submit_button("Add Goal", use_container_width=True):
            add_goal(goal_name, goal_target)
            st.success("Goal added!")

    goals = get_goals()
    if not goals.empty:
        st.markdown("### Your Goals")
        for _, goal in goals.iterrows():
            progress = (goal['saved'] / goal['target']) * 100 if goal['target'] > 0 else 0
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{goal['name']}**")
                    st.progress(min(progress/100, 1.0))
                    st.caption(f"₹{goal['saved']:,.0f} / ₹{goal['target']:,.0f} ({progress:.1f}%)")
                with col2:
                    new_saved = st.number_input(f"Add to {goal['name']}", min_value=0, key=f"add_{goal['id']}")
                    if st.button("Update", key=f"upd_{goal['id']}"):
                        update_goal_saved(goal['id'], goal['saved'] + new_saved)
                        st.rerun()
                with col3:
                    if st.button("🗑️ Delete", key=f"delg_{goal['id']}"):
                        delete_goal(goal['id'])
                        st.rerun()
                st.markdown("---")
