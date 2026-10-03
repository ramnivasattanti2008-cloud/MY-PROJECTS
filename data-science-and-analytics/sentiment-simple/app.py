"""
Sentiment Analyzer - Streamlit Web App
A simple web interface to analyze the sentiment of text using TextBlob.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="💬",
    layout="centered"
)

# Custom dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #ff6b9d !important;
    }
    .sentiment-positive {
        background: linear-gradient(135deg, #1a4d2e 0%, #2d6a4f 100%);
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #00ff88;
        text-align: center;
        margin: 20px 0;
    }
    .sentiment-negative {
        background: linear-gradient(135deg, #4d1a1a 0%, #6b2d2d 100%);
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #ff4444;
        text-align: center;
        margin: 20px 0;
    }
    .sentiment-neutral {
        background: linear-gradient(135deg, #1a2e4d 0%, #2d4a6b 100%);
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #4da6ff;
        text-align: center;
        margin: 20px 0;
    }
    .emoji-large {
        font-size: 80px;
        margin: 10px 0;
    }
    .score-display {
        font-size: 48px;
        font-weight: bold;
        margin: 10px 0;
    }
    .word-analysis {
        background-color: #1e2530;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


def get_sentiment(text):
    """
    Analyze sentiment using TextBlob.

    TextBlob uses a pre-trained sentiment analyzer that returns:
    - polarity: -1 (negative) to +1 (positive)
    - subjectivity: 0 (objective) to 1 (subjective)

    Args:
        text: The text to analyze

    Returns:
        dict with polarity, subjectivity, and sentiment category
    """
    from textblob import TextBlob

    blob = TextBlob(text)

    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    # Classify sentiment
    if polarity > 0.1:
        category = "positive"
    elif polarity < -0.1:
        category = "negative"
    else:
        category = "neutral"

    return {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "category": category,
        "blob": blob,
        "word_count": len(blob.words),
        "sentence_count": len(blob.sentences)
    }


def get_word_sentiments(blob):
    """
    Get sentiment scores for individual words.
    Returns list of (word, sentiment) tuples.
    """
    word_sentiments = []
    for word in blob.words:
        word_polarity = TextBlob(str(word)).sentiment.polarity
        if word_polarity != 0:
            word_sentiments.append((str(word), word_polarity))

    # Sort by absolute polarity
    word_sentiments.sort(key=lambda x: abs(x[1]), reverse=True)
    return word_sentiments[:10]  # Top 10 most sentimental words


def main():
    # Header
    st.markdown("# 💬 Sentiment Analyzer")
    st.markdown("*Analyze the emotion behind any text*")
    st.divider()

    # Input section
    st.markdown("### 📝 Enter Text to Analyze")

    text = st.text_area(
        "Type or paste your text here:",
        height=150,
        placeholder="e.g., 'I absolutely love this product! It works perfectly and exceeded my expectations.'"
    )

    # Analyze button
    if st.button("🔍 Analyze Sentiment", type="primary", use_container_width=True):
        if text.strip():
            with st.spinner("Analyzing..."):
                result = get_sentiment(text)

            # Display result based on sentiment
            st.divider()

            if result["category"] == "positive":
                st.markdown(f"""
                <div class="sentiment-positive">
                    <div class="emoji-large">😊</div>
                    <div class="score-display" style="color: #00ff88;">POSITIVE</div>
                    <div style="font-size: 18px; color: #aaa;">
                        Polarity Score: {result['polarity']:.2f} / 1.0
                    </div>
                </div>
                """, unsafe_allow_html=True)
                emoji = "positive"
            elif result["category"] == "negative":
                st.markdown(f"""
                <div class="sentiment-negative">
                    <div class="emoji-large">😞</div>
                    <div class="score-display" style="color: #ff4444;">NEGATIVE</div>
                    <div style="font-size: 18px; color: #aaa;">
                        Polarity Score: {result['polarity']:.2f} / 1.0
                    </div>
                </div>
                """, unsafe_allow_html=True)
                emoji = "negative"
            else:
                st.markdown(f"""
                <div class="sentiment-neutral">
                    <div class="emoji-large">😐</div>
                    <div class="score-display" style="color: #4da6ff;">NEUTRAL</div>
                    <div style="font-size: 18px; color: #aaa;">
                        Polarity Score: {result['polarity']:.2f} / 1.0
                    </div>
                </div>
                """, unsafe_allow_html=True)
                emoji = "neutral"

            # Detailed metrics
            st.markdown("### 📊 Detailed Analysis")

            col1, col2, col3 = st.columns(3)

            with col1:
                # Polarity gauge
                st.markdown("#### Polarity")
                # Visual polarity bar
                if result["polarity"] >= 0:
                    positive_width = result["polarity"] * 100
                    st.markdown(
                        f'<div style="background-color: #333; border-radius: 10px; overflow: hidden; height: 30px;">'
                        f'<div style="background-color: #00ff88; width: {positive_width}%; height: 100%;"></div></div>',
                        unsafe_allow_html=True
                    )
                else:
                    negative_width = abs(result["polarity"]) * 100
                    st.markdown(
                        f'<div style="background-color: #333; border-radius: 10px; overflow: hidden; height: 30px;">'
                        f'<div style="background-color: #ff4444; width: {negative_width}%; height: 100%; margin-left: auto;"></div></div>',
                        unsafe_allow_html=True
                    )
                st.markdown(f"**{result['polarity']:.2f}** (range: -1 to +1)")

            with col2:
                st.markdown("#### Subjectivity")
                subj_pct = result["subjectivity"] * 100
                st.markdown(
                    f'<div style="background-color: #333; border-radius: 10px; overflow: hidden; height: 30px;">'
                    f'<div style="background-color: #ff6b9d; width: {subj_pct}%; height: 100%;"></div></div>',
                    unsafe_allow_html=True
                )
                st.markdown(f"**{subj_pct:.0f}%** subjective")
                if result["subjectivity"] < 0.4:
                    st.caption("📋 More objective/factual")
                else:
                    st.caption("💭 More personal opinion")

            with col3:
                st.markdown("#### Text Stats")
                st.markdown(f"**Words:** {result['word_count']}")
                st.markdown(f"**Sentences:** {result['sentence_count']}")
                st.markdown(f"**Avg words/sentence:** {result['word_count']/max(1, result['sentence_count']):.1f}")

            # Word-level analysis
            st.divider()
            st.markdown("### 🔤 Word-Level Sentiment")

            word_sentiments = get_word_sentiments(result["blob"])

            if word_sentiments:
                st.markdown("**Most impactful words:**")
                for word, score in word_sentiments[:5]:
                    color = "#00ff88" if score > 0 else "#ff4444"
                    sign = "+" if score > 0 else ""
                    st.markdown(
                        f'<div style="display: flex; justify-content: space-between; padding: 5px 0; '
                        f'border-bottom: 1px solid #333;">'
                        f'<span>{word}</span>'
                        f'<span style="color: {color};">{sign}{score:.2f}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.info("No strongly sentiment words detected (neutral text)")

            # Visual sentiment indicator
            st.divider()
            st.markdown("### 📈 Sentiment Meter")

            # Create a visual scale
            scale_col1, scale_col2, scale_col3, scale_col4, scale_col5 = st.columns(5)

            with scale_col1:
                st.markdown("😞<br>Very<br>Negative", unsafe_allow_html=True)
            with scale_col2:
                st.markdown("😟<br>Negative", unsafe_allow_html=True)
            with scale_col3:
                st.markdown("😐<br>Neutral", unsafe_allow_html=True)
            with scale_col4:
                st.markdown("😊<br>Positive", unsafe_allow_html=True)
            with scale_col5:
                st.markdown("😄<br>Very<br>Positive", unsafe_allow_html=True)

            # Position marker
            position = (result["polarity"] + 1) / 2 * 100  # Convert -1..1 to 0..100

            st.markdown(
                f'<div style="background-color: #333; border-radius: 10px; overflow: hidden; height: 40px; position: relative;">'
                f'<div style="background: linear-gradient(90deg, #ff4444, #ffaa00, #888, #00aa00, #00ff00); '
                f'width: 100%; height: 100%;"></div>'
                f'<div style="position: absolute; top: -10px; left: {position}%; transform: translateX(-50%); '
                f'font-size: 24px;">🔺</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        else:
            st.warning("Please enter some text to analyze.")

    # Example texts
    st.divider()
    st.markdown("### 💡 Try These Examples")

    examples = [
        ("Positive Review", "This product is absolutely amazing! I love it so much. Best purchase ever!"),
        ("Negative Review", "Terrible experience. Complete waste of money. Never buying again."),
        ("Neutral Statement", "The meeting is scheduled for 3pm tomorrow in conference room B."),
        ("Mixed Review", "The food was good but the service was slow. Would probably go back though."),
        ("Opinion", "I personally think this could be better, but others seem to like it."),
    ]

    for label, example_text in examples:
        if st.button(f"📝 {label}", key=f"ex_{label}", use_container_width=True):
            st.session_state.example_text = example_text
            st.rerun()

    # Info section
    st.divider()
    st.markdown("""
    <div style="background-color: #1e2530; padding: 15px; border-radius: 8px; border-left: 4px solid #ff6b9d;">
    <strong>How It Works:</strong><br><br>
    This analyzer uses <strong>TextBlob</strong>, a Python library for processing textual data.
    It uses a pre-trained sentiment analyzer that assigns polarity scores (-1 to +1) based on
    the emotional tone of words in the text.<br><br>
    <strong>Polarity:</strong> Measures how positive or negative the text is<br>
    <strong>Subjectivity:</strong> Measures how much opinion vs. factual information is present
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
