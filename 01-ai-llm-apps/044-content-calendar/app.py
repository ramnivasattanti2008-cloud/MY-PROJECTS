import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Content Calendar", page_icon="", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%); }
.stButton>button { background: linear-gradient(90deg, #00d9ff, #00ff88); color: #1a1a2e; border: none; border-radius: 25px; font-weight: bold; }
.stSelectbox>div, .stDateInput>div { background: #0f3460 !important; border-radius: 12px; }
h1, h2 { color: #00d9ff !important; }
[data-testid="stMetricValue"] { color: #00ff88 !important; }
.stExpander { background: #16213e !important; border-radius: 12px; border: 1px solid #00d9ff; }
</style>
""", unsafe_allow_html=True)

st.title("  Social Media Content Calendar")
st.caption("Plan, schedule, and track your content")

if "posts" not in st.session_state:
    st.session_state.posts = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(" Total Posts", len(st.session_state.posts))
with col2:
    scheduled = sum(1 for p in st.session_state.posts if p["status"] == "Scheduled")
    st.metric(" Scheduled", scheduled)
with col3:
    published = sum(1 for p in st.session_state.posts if p["status"] == "Published")
    st.metric(" Published", published)
with col4:
    draft = sum(1 for p in st.session_state.posts if p["status"] == "Draft")
    st.metric(" Drafts", draft)

with st.expander("  Add New Post", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        platform = st.selectbox(" Platform", ["Twitter", "Instagram", "LinkedIn", "Facebook"])
        date = st.date_input(" Publish Date", datetime.today())
        time = st.time_input(" Publish Time", datetime.now().time())
    with c2:
        status = st.selectbox(" Status", ["Draft", "Scheduled", "Published"])
        content = st.text_area(" Content", placeholder="What's on your mind?")
        tags = st.text_input(" Hashtags/Tags", placeholder="#marketing #growth")

    if st.button("  Add Post"):
        post = {"id": len(st.session_state.posts) + 1, "platform": platform,
                "date": str(date), "time": str(time), "status": status,
                "content": content[:100] + "..." if len(content) > 100 else content,
                "tags": tags, "likes": 0, "comments": 0}
        st.session_state.posts.append(post)
        st.success(" Post added!")

if st.session_state.posts:
    df = pd.DataFrame(st.session_state.posts)
    st.dataframe(df[["platform", "date", "status", "content", "tags"]], use_container_width=True)

    st.subheader("  Update Engagement")
    post_ids = [str(p["id"]) for p in st.session_state.posts]
    selected = st.selectbox(" Select Post", post_ids)
    likes = st.number_input(" Likes", min_value=0, value=0)
    comments = st.number_input(" Comments", min_value=0, value=0)
    if st.button("  Update Stats"):
        for p in st.session_state.posts:
            if str(p["id"]) == selected:
                p["likes"] = likes
                p["comments"] = comments
        st.success(" Stats updated!")
else:
    st.info("  No posts yet. Add your first post above!")

st.markdown("---")
st.markdown("  *Built with Streamlit*", unsafe_allow_html=True)
