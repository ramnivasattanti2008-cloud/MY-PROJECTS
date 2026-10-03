import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Review Summarizer", page_icon="⭐", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .sentiment-positive { color: #3fb950; }
    .sentiment-negative { color: #f85149; }
    .sentiment-neutral { color: #d29922; }
    .summary-box { background-color: #161b22; padding: 20px; border-radius: 10px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.title("⭐ Product Review Summarizer")
st.caption("Paste reviews, get instant insights on common themes and sentiment")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password",
                           value=os.environ.get("GEMINI_API_KEY", ""))
    st.caption("Get your key at [Google AI Studio](https://aistudio.google.com/)")

    st.divider()
    st.subheader("📊 Analysis Options")
    analysis_depth = st.selectbox("Analysis Depth", ["Quick Summary", "Detailed Analysis"])
    show_examples = st.checkbox("Include Review Examples", value=True)

    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key")

# Main content
st.markdown("### 📋 Paste Product Reviews")
st.caption("Paste one review per line, or separate with blank lines")

reviews_input = st.text_area(
    "Reviews",
    height=300,
    placeholder="""Great product! Exactly what I was looking for. Fast shipping too.
The quality is poor and it broke after one week. Very disappointed.
Love it! Works perfectly and the customer service was helpful when I had questions.
Average product. Does the job but nothing special. Overpriced for what you get.
Would highly recommend to anyone looking for quality at a fair price."""
)

product_name = st.text_input("Product Name (optional)", placeholder="Smart Watch Pro X")

if st.button("🔍 Analyze Reviews", type="primary", disabled=not api_key):
    if not reviews_input.strip():
        st.error("❌ Please paste at least one review")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            product_context = f" for {product_name}" if product_name else ""
            depth_instruction = "Provide a detailed breakdown" if analysis_depth == "Detailed Analysis" else "Provide a concise summary"

            prompt = f"""{depth_instruction} of these product reviews{product_context}.

Reviews:
{reviews_input}

Analyze and return:
1. **Overall Sentiment** - Positive, Negative, or Mixed (with percentage)
2. **Key Themes** - Common praise points and common complaints
3. **Pros & Cons** - Top 3-5 of each
4. **Rating Breakdown** - Estimate of star distribution
5. **Target Customer** - Who would love / hate this product
{f'6. **Notable Quotes** - 2-3 representative review excerpts' if show_examples else ''}

Be specific and actionable in your insights."""

            with st.spinner("🔬 Analyzing sentiment..."):
                response = model.generate_content(prompt)

            st.success("✅ Analysis Complete!")

            # Display results
            st.markdown("### 📊 Summary Results")
            st.markdown(f"""
            <div class="summary-box">
            {response.text.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown(response.text)

            # Quick stats
            st.markdown("### 📈 Quick Stats")
            reviews = [r.strip() for r in reviews_input.split('\n') if r.strip()]
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Reviews", len(reviews))
            col2.metric("Analysis Type", analysis_depth)
            col3.metric("Product", product_name if product_name else "General")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider()
st.caption("💡 Tip: More reviews = more accurate insights! Paste at least 10 for best results.")
