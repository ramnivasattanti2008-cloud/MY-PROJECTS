import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Reading List", page_icon="📖", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .metric-card { background-color: #1e2530; padding: 20px; border-radius: 10px; text-align: center; }
    .book-card { background-color: #1e2530; padding: 15px; border-radius: 10px; margin: 10px 0; }
    .stars { color: #fbbf24; }
    h1, h2, h3 { color: #ffffff !important; }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div {
        background-color: #1e2530; color: white; border: 1px solid #3d4654;
    }
</style>
""", unsafe_allow_html=True)

GENRES = ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery",
          "Biography", "Self-Help", "History", "Science", "Technology", "Romance", "Other"]

STATUS_OPTIONS = ["To Read", "Reading", "Completed"]

def init_db():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT,
                  genre TEXT, status TEXT, rating INTEGER, notes TEXT, added_date TEXT)''')
    conn.commit()
    conn.close()

def get_books():
    conn = sqlite3.connect('books.db')
    df = pd.read_sql('SELECT * FROM books ORDER BY added_date DESC', conn)
    conn.close()
    return df

def add_book(title, author, genre, status, notes):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('INSERT INTO books (title, author, genre, status, notes, added_date) VALUES (?, ?, ?, ?, ?, ?)',
              (title, author, genre, status, notes, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def update_book(book_id, status=None, rating=None, notes=None):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    if status is not None:
        c.execute('UPDATE books SET status = ? WHERE id = ?', (status, book_id))
    if rating is not None:
        c.execute('UPDATE books SET rating = ? WHERE id = ?', (rating, book_id))
    if notes is not None:
        c.execute('UPDATE books SET notes = ? WHERE id = ?', (notes, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

def render_stars(rating):
    if rating and rating > 0:
        return "⭐" * rating + "☆" * (5 - rating)
    return "Not rated"

init_db()

st.title("📖 Reading List Manager")
st.markdown("---")

books = get_books()

# Stats
total = len(books)
to_read = len(books[books['status'] == 'To Read']) if not books.empty else 0
reading = len(books[books['status'] == 'Reading']) if not books.empty else 0
completed = len(books[books['status'] == 'Completed']) if not books.empty else 0
avg_rating = books[books['rating'].notna() & (books['rating'] > 0)]['rating'].mean() if not books.empty else 0

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"<div class='metric-card'><h3>Total Books</h3><h2 style='color:#60a5fa'>{total}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h3>To Read</h3><h2 style='color:#a78bfa'>{to_read}</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h3>Reading</h3><h2 style='color:#fbbf24'>{reading}</h2></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><h3>Completed</h3><h2 style='color:#4ade80'>{completed}</h2></div>", unsafe_allow_html=True)
with col5:
    st.markdown(f"<div class='metric-card'><h3>Avg Rating</h3><h2 style='color:#fbbf24'>{avg_rating:.1f}/5</h2></div>", unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📚 Add Book", "📋 All Books", "📊 Statistics", "🔍 Search"])

with tab1:
    st.header("Add a New Book")
    with st.form("book_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Book Title", placeholder="e.g., Atomic Habits")
            author = st.text_input("Author", placeholder="e.g., James Clear")
            genre = st.selectbox("Genre", GENRES)
        with col2:
            status = st.selectbox("Status", STATUS_OPTIONS)
            notes = st.text_area("Notes (optional)", placeholder="Why you want to read this...")
        if st.form_submit_button("Add Book", use_container_width=True):
            if title and author:
                add_book(title, author, genre, status, notes)
                st.success("Book added to your list!")
            else:
                st.error("Title and Author are required!")

with tab2:
    st.header("Your Reading List")
    filter_status = st.selectbox("Filter by Status", ["All"] + STATUS_OPTIONS)

    display_books = books if filter_status == "All" else books[books['status'] == filter_status]

    if not display_books.empty:
        for _, book in display_books.iterrows():
            status_color = {"To Read": "#a78bfa", "Reading": "#fbbf24", "Completed": "#4ade80"}
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"### {book['title']}")
                    st.markdown(f"**Author:** {book['author']} | **Genre:** {book['genre']}")
                    st.markdown(f"<span style='color:{status_color.get(book['status'], '#fff')}'>{book['status']}</span> | {render_stars(book['rating'])}", unsafe_allow_html=True)
                    if book['notes']:
                        st.caption(f"📝 {book['notes'][:100]}...")
                with col2:
                    new_status = st.selectbox("Status", STATUS_OPTIONS,
                                            index=STATUS_OPTIONS.index(book['status']) if book['status'] in STATUS_OPTIONS else 0,
                                            key=f"status_{book['id']}")
                    new_rating = st.slider("Rating", 0, 5, int(book['rating']) if book['rating'] else 0, key=f"rating_{book['id']}")
                    if st.button("Update", key=f"upd_{book['id']}"):
                        update_book(book['id'], status=new_status, rating=new_rating)
                        st.rerun()
                with col3:
                    if st.button("🗑️ Delete", key=f"del_{book['id']}"):
                        delete_book(book['id'])
                        st.rerun()
                st.markdown("---")
    else:
        st.info("No books in this category. Add some books!")

with tab3:
    st.header("Reading Statistics")
    if not books.empty:
        col1, col2 = st.columns(2)

        with col1:
            # Books by status
            status_counts = books['status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            fig = px.pie(status_counts, names='Status', values='Count', title="Books by Status")
            fig.update_layout(plot_bgcolor='#1e2530', paper_bgcolor='#0e1117', font_color='white')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Books by genre
            genre_counts = books['genre'].value_counts().reset_index()
            genre_counts.columns = ['Genre', 'Count']
            genre_counts = genre_counts.sort_values('Count', ascending=True)
            fig2 = px.bar(genre_counts, y='Genre', x='Count', orientation='h', title="Books by Genre", color='Count', color_continuous_scale='Viridis')
            fig2.update_layout(plot_bgcolor='#1e2530', paper_bgcolor='#0e1117', font_color='white')
            st.plotly_chart(fig2, use_container_width=True)

        # Rating distribution
        rated = books[books['rating'].notna() & (books['rating'] > 0)]
        if not rated.empty:
            fig3 = px.histogram(rated, x='rating', nbins=5, title="Rating Distribution",
                               labels={'rating': 'Rating', 'count': 'Number of Books'})
            fig3.update_layout(plot_bgcolor='#1e2530', paper_bgcolor='#0e1117', font_color='white')
            fig3.update_traces(marker_color='#fbbf24')
            st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Add some books to see statistics!")

with tab4:
    st.header("Search Books")
    search = st.text_input("🔍 Search by title or author...", placeholder="Type to search...")

    if search:
        results = books[
            books['title'].str.contains(search, case=False, na=False) |
            books['author'].str.contains(search, case=False, na=False)
        ]

        if not results.empty:
            st.markdown(f"### Found {len(results)} book(s)")
            for _, book in results.iterrows():
                st.markdown(f"**{book['title']}** by {book['author']} - {book['status']} {render_stars(book['rating'])}")
        else:
            st.info("No books found matching your search.")
    else:
        st.info("Enter a search term to find books.")
