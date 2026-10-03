"""
Sales Dashboard
A Streamlit application for analyzing sales data with interactive visualizations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📈",
    layout="wide"
)

# Dark theme styling
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .css-1d391kg { padding: 2rem; }
    h1, h2, h3 { color: #ffffff; }
    .kpi-card { background-color: #1e2530; padding: 1.5rem; border-radius: 10px; text-align: center; }
    .kpi-value { font-size: 2.5rem; font-weight: bold; color: #00d4aa; }
    .kpi-label { font-size: 0.9rem; color: #888; }
</style>
""", unsafe_allow_html=True)

def generate_sample_data():
    """Generate sample sales data"""
    np.random.seed(42)
    n_records = 500

    # Generate date range (last 12 months)
    end_date = datetime.now()
    dates = [end_date - timedelta(days=np.random.randint(0, 365)) for _ in range(n_records)]

    regions = ['North', 'South', 'East', 'West', 'Central']
    products = ['Laptop', 'Desktop', 'Tablet', 'Phone', 'Accessories', 'Software', 'Services']
    categories = ['Electronics', 'Accessories', 'Software', 'Services']

    data = {
        'date': dates,
        'region': np.random.choice(regions, n_records),
        'product': np.random.choice(products, n_records),
        'category': np.random.choice(categories, n_records),
        'quantity': np.random.randint(1, 50, n_records),
        'unit_price': np.random.uniform(10, 2000, n_records).round(2),
        'customer_type': np.random.choice(['Individual', 'Business', 'Government'], n_records),
        'salesperson': np.random.choice(['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'], n_records)
    }

    df = pd.DataFrame(data)
    df['revenue'] = df['quantity'] * df['unit_price']
    df['date'] = pd.to_datetime(df['date'])

    return df

def main():
    st.title("📈 Sales Dashboard")
    st.markdown("### Upload your sales data or use sample data to analyze performance")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select View",
        ["Overview", "Revenue Analysis", "Product Analysis", "Regional Analysis", "Time Analysis"]
    )

    # Check if data is loaded
    if 'df' not in st.session_state:
        st.session_state.df = None

    # File upload
    with st.expander("📁 Upload Sales Data", expanded=True):
        uploaded_file = st.file_uploader(
            "Choose a CSV file with sales data",
            type=['csv'],
            help="CSV should have columns: date, region, product, quantity, unit_price"
        )

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                df['date'] = pd.to_datetime(df['date'])
                if 'revenue' not in df.columns:
                    df['revenue'] = df['quantity'] * df['unit_price']
                st.session_state.df = df
                st.success(f"Loaded {len(df)} sales records")

                with st.expander("Preview Data"):
                    st.dataframe(df.head(10), use_container_width=True)
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

    # Sample data option
    if st.session_state.df is None:
        col1, col2 = st.columns(2)
        with col1:
            st.info("👆 Please upload a CSV file or load sample data")
        with col2:
            if st.button("📊 Load Sample Data"):
                df = generate_sample_data()
                st.session_state.df = df
                st.success("Sample sales data loaded!")

    if st.session_state.df is not None:
        df = st.session_state.df

        if page == "Overview":
            show_overview(df)
        elif page == "Revenue Analysis":
            show_revenue_analysis(df)
        elif page == "Product Analysis":
            show_product_analysis(df)
        elif page == "Regional Analysis":
            show_regional_analysis(df)
        elif page == "Time Analysis":
            show_time_analysis(df)

def show_overview(df):
    """Display overview KPIs"""
    st.header("📊 Sales Overview")

    # Calculate KPIs
    total_revenue = df['revenue'].sum()
    total_orders = len(df)
    avg_order_value = df['revenue'].mean()
    total_quantity = df['quantity'].sum()

    # Display KPI cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">${total_revenue:,.0f}</div>
            <div class="kpi-label">Total Revenue</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-label">Total Orders</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">${avg_order_value:,.0f}</div>
            <div class="kpi-label">Avg Order Value</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{total_quantity:,}</div>
            <div class="kpi-label">Units Sold</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Quick stats
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Products by Revenue")
        top_products = df.groupby('product')['revenue'].sum().sort_values(ascending=False).head(5)
        fig = px.bar(
            x=top_products.index,
            y=top_products.values,
            color=top_products.values,
            color_continuous_scale='Viridis',
            text=top_products.values.round(0)
        )
        fig.update_layout(template='plotly_dark', height=400)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Revenue by Region")
        region_revenue = df.groupby('region')['revenue'].sum().sort_values(ascending=False)
        fig = px.pie(
            values=region_revenue.values,
            names=region_revenue.index,
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Recent transactions
    st.subheader("Recent Transactions")
    recent = df.sort_values('date', ascending=False).head(10)
    st.dataframe(recent, use_container_width=True)

def show_revenue_analysis(df):
    """Detailed revenue analysis"""
    st.header("💰 Revenue Analysis")

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        regions = ['All'] + df['region'].unique().tolist()
        selected_region = st.selectbox("Region", regions)

    with col2:
        categories = ['All'] + df['category'].unique().tolist()
        selected_category = st.selectbox("Category", categories)

    with col3:
        products = ['All'] + df['product'].unique().tolist()
        selected_product = st.selectbox("Product", products)

    # Apply filters
    filtered_df = df.copy()
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    if selected_product != 'All':
        filtered_df = filtered_df[filtered_df['product'] == selected_product]

    # Filtered KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Revenue", f"${filtered_df['revenue'].sum():,.0f}")

    with col2:
        st.metric("Orders", len(filtered_df))

    with col3:
        st.metric("Avg Order", f"${filtered_df['revenue'].mean():,.0f}")

    with col4:
        st.metric("Units Sold", filtered_df['quantity'].sum())

    st.divider()

    # Revenue breakdown
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by Category")
        cat_revenue = filtered_df.groupby('category')['revenue'].sum().sort_values(ascending=True)
        fig = px.barh(
            x=cat_revenue.values,
            y=cat_revenue.index,
            color=cat_revenue.values,
            color_continuous_scale='Greens'
        )
        fig.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Revenue by Customer Type")
        customer_revenue = filtered_df.groupby('customer_type')['revenue'].sum()
        fig = px.pie(
            values=customer_revenue.values,
            names=customer_revenue.index,
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Revenue by salesperson
    st.subheader("Revenue by Salesperson")
    sales_person = filtered_df.groupby('salesperson').agg({
        'revenue': 'sum',
        'quantity': 'sum',
        'date': 'count'
    }).rename(columns={'date': 'orders'}).sort_values('revenue', ascending=False)

    fig = px.bar(
        x=sales_person.index,
        y=sales_person['revenue'],
        color=sales_person['revenue'],
        color_continuous_scale='Blues',
        text=sales_person['revenue'].round(0)
    )
    fig.update_layout(template='plotly_dark', height=400)
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

def show_product_analysis(df):
    """Product performance analysis"""
    st.header("📦 Product Analysis")

    # Product performance table
    product_stats = df.groupby('product').agg({
        'revenue': 'sum',
        'quantity': 'sum',
        'date': 'count'
    }).rename(columns={'date': 'orders'})
    product_stats['avg_order_value'] = product_stats['revenue'] / product_stats['orders']
    product_stats = product_stats.sort_values('revenue', ascending=False)

    st.dataframe(
        product_stats.style.background_gradient(subset=['revenue'], cmap='Greens'),
        use_container_width=True
    )

    st.divider()

    # Product comparison
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Quantity Sold by Product")
        product_qty = df.groupby('product')['quantity'].sum().sort_values(ascending=True)
        fig = px.barh(
            x=product_qty.values,
            y=product_qty.index,
            color=product_qty.values,
            color_continuous_scale='Oranges'
        )
        fig.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Average Order Value by Product")
        product_avg = df.groupby('product')['revenue'].mean().sort_values(ascending=True)
        fig = px.barh(
            x=product_avg.values,
            y=product_avg.index,
            color=product_avg.values,
            color_continuous_scale='Purples'
        )
        fig.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Product by region heatmap
    st.subheader("Product Performance by Region")
    pivot = df.pivot_table(values='revenue', index='product', columns='region', aggfunc='sum', fill_value=0)

    fig = px.imshow(
        pivot,
        labels=dict(x="Region", y="Product", color="Revenue"),
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(template='plotly_dark', height=500)
    st.plotly_chart(fig, use_container_width=True)

def show_regional_analysis(df):
    """Regional performance analysis"""
    st.header("🗺️ Regional Analysis")

    # Region summary
    region_stats = df.groupby('region').agg({
        'revenue': 'sum',
        'quantity': 'sum',
        'date': 'count'
    }).rename(columns={'date': 'orders'})
    region_stats['avg_order'] = region_stats['revenue'] / region_stats['orders']
    region_stats = region_stats.sort_values('revenue', ascending=False)

    st.dataframe(
        region_stats.style.background_gradient(subset=['revenue'], cmap='Blues'),
        use_container_width=True
    )

    st.divider()

    # Regional comparison
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by Region")
        fig = px.bar(
            x=region_stats.index,
            y=region_stats['revenue'],
            color=region_stats['revenue'],
            color_continuous_scale='Viridis',
            text=region_stats['revenue'].round(0)
        )
        fig.update_layout(template='plotly_dark', height=400)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Orders by Region")
        fig = px.bar(
            x=region_stats.index,
            y=region_stats['orders'],
            color=region_stats['orders'],
            color_continuous_scale='Plasma',
            text=region_stats['orders']
        )
        fig.update_layout(template='plotly_dark', height=400)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    # Regional product breakdown
    st.subheader("Top Products by Region")
    for region in df['region'].unique():
        st.markdown(f"**{region}**")
        region_data = df[df['region'] == region].groupby('product')['revenue'].sum().sort_values(ascending=False).head(3)
        for product, revenue in region_data.items():
            st.write(f"  - {product}: ${revenue:,.0f}")

def show_time_analysis(df):
    """Time-based analysis"""
    st.header("📅 Time Analysis")

    # Add time columns
    df['month'] = df['date'].dt.to_period('M').astype(str)
    df['week'] = df['date'].dt.isocalendar().week
    df['day_of_week'] = df['date'].dt.day_name()
    df['quarter'] = df['date'].dt.quarter

    # Time period selector
    period = st.selectbox("Time Period", ["Monthly", "Weekly", "Quarterly", "Day of Week"])

    if period == "Monthly":
        time_col = 'month'
        x_label = "Month"
    elif period == "Weekly":
        time_col = 'week'
        x_label = "Week"
    elif period == "Quarterly":
        time_col = 'quarter'
        x_label = "Quarter"
    else:
        time_col = 'day_of_week'
        x_label = "Day"

    # Time-based revenue
    time_revenue = df.groupby(time_col)['revenue'].sum().reset_index()
    time_revenue = time_revenue.sort_values(time_col)

    fig = px.line(
        time_revenue,
        x=time_col,
        y='revenue',
        markers=True,
        line_shape='spline'
    )
    fig.update_traces(line=dict(color='#00d4aa', width=3))
    fig.update_layout(template='plotly_dark', height=400, xaxis_title=x_label, yaxis_title="Revenue")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Comparison charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Orders Over Time")
        time_orders = df.groupby(time_col)['date'].count().reset_index()
        time_orders.columns = [time_col, 'orders']
        time_orders = time_orders.sort_values(time_col)

        fig = px.bar(
            time_orders,
            x=time_col,
            y='orders',
            color='orders',
            color_continuous_scale='Blues'
        )
        fig.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Average Order Value Over Time")
        time_avg = df.groupby(time_col)['revenue'].mean().reset_index()
        time_avg.columns = [time_col, 'avg_order']
        time_avg = time_avg.sort_values(time_col)

        fig = px.area(
            time_avg,
            x=time_col,
            y='avg_order',
            color_discrete_sequence=['#ff6b6b']
        )
        fig.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Trend analysis
    st.subheader("Growth Trend")

    time_revenue_sorted = time_revenue.sort_values(time_col)
    time_revenue_sorted['growth'] = time_revenue_sorted['revenue'].pct_change() * 100

    fig = px.bar(
        time_revenue_sorted.dropna(),
        x=time_col,
        y='growth',
        color='growth',
        color_continuous_scale='RdYlGn',
        text=time_revenue_sorted['growth'].dropna().round(1)
    )
    fig.update_layout(template='plotly_dark', height=400)
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
