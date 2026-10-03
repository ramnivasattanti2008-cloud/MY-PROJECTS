import streamlit as st
import markdown
from datetime import datetime
import io

st.set_page_config(page_title="Markdown Editor", page_icon="📝", layout="wide")

st.title("Markdown Editor")
st.markdown("Write Markdown and see live preview, or export to HTML")

default_text = """# Welcome to Markdown Editor

This is a **live preview** editor. Start typing your Markdown on the left and see the rendered output on the right.

## Features

- **Live Preview** - See your changes instantly
- **Export to HTML** - Download your document as an HTML file
- **Syntax Highlighting** - Full Markdown support

## Text Formatting

You can make text **bold**, *italic*, or ***both***.

> This is a blockquote for important notes.

## Lists

### Unordered List
- Item one
- Item two
- Item three

### Ordered List
1. First step
2. Second step
3. Third step

## Code

Inline code: `print("Hello World")`

Code block:
```python
def hello():
    print("Hello, World!")
```

## Tables

| Feature | Status |
|---------|--------|
| Live Preview | ✅ |
| Export HTML | ✅ |
| Dark Mode | ✅ |

## Links and Images

[Visit Example](https://example.com)

---

*Start editing on the left panel!*
"""

if 'content' not in st.session_state:
    st.session_state.content = default_text

with st.sidebar:
    st.header("Settings")

    theme = st.selectbox("Theme", ["Light", "Dark"])

    st.divider()

    st.header("Document Info")

    char_count = len(st.session_state.content)
    word_count = len(st.session_state.content.split())
    line_count = st.session_state.content.count('\n') + 1

    st.metric("Characters", char_count)
    st.metric("Words", word_count)
    st.metric("Lines", line_count)

    st.divider()

    st.header("Export")

    col1, col2 = st.columns(2)

    with col1:
        html_filename = st.text_input("Filename", value="document")
        if not html_filename.endswith('.html'):
            html_filename += '.html'

    with col2:
        pass

    custom_css = st.checkbox("Include custom styling")

    if st.button("Export HTML", use_container_width=True):
        html_content = markdown.markdown(
            st.session_state.content,
            extensions=['fenced_code', 'tables', 'blockquote', 'nl2br']
        )

        if custom_css:
            full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_filename.replace('.html', '')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.6;
            {'background: #1a1a2e; color: #eee;' if theme == 'Dark' else 'background: #fff; color: #333;'}
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }}
        code {{
            background: {'#2d2d44' if theme == 'Dark' else '#f4f4f4'};
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: monospace;
        }}
        pre {{
            background: {'#2d2d44' if theme == 'Dark' else '#f4f4f4'};
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid {'#e94560' if theme == 'Dark' else '#ff6b35'};
            margin: 1rem 0;
            padding-left: 1rem;
            color: {'#aaa' if theme == 'Dark' else '#666'};
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }}
        th, td {{
            border: 1px solid {'#444' if theme == 'Dark' else '#ddd'};
            padding: 0.75rem;
            text-align: left;
        }}
        th {{
            background: {'#2d2d44' if theme == 'Dark' else '#f4f4f4'};
        }}
        a {{
            color: {'#e94560' if theme == 'Dark' else '#ff6b35'};
        }}
        hr {{
            border: none;
            border-top: 2px solid {'#444' if theme == 'Dark' else '#ddd'};
            margin: 2rem 0;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        else:
            full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_filename.replace('.html', '')}</title>
</head>
<body>
{html_content}
</body>
</html>"""

        st.download_button(
            label="Download HTML",
            data=full_html,
            file_name=html_filename,
            mime="text/html",
            use_container_width=True
        )

    st.divider()

    if st.button("Clear Document", use_container_width=True):
        st.session_state.content = ""
        st.rerun()

    if st.button("Load Sample", use_container_width=True):
        st.session_state.content = default_text
        st.rerun()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Editor")

    new_content = st.text_area(
        "Write your Markdown here...",
        value=st.session_state.content,
        height=600,
        key="editor",
        label_visibility="collapsed"
    )

    st.session_state.content = new_content

with col2:
    st.subheader("👁️ Preview")

    if theme == "Dark":
        st.markdown("""
        <style>
        .stMarkdown {
            background: #1a1a2e;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #333;
            color: #eee;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: #1a1a2e; padding: 1.5rem; border-radius: 8px; border: 1px solid #333; color: #eee;">
            {markdown.markdown(st.session_state.content, extensions=['fenced_code', 'tables', 'blockquote', 'nl2br'])}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(st.session_state.content, unsafe_allow_html=False)

st.divider()

with st.expander("📚 Markdown Quick Reference"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Headers**
        ```markdown
        # H1
        ## H2
        ### H3
        ```

        **Emphasis**
        ```markdown
        **bold**
        *italic*
        ***both***
        ```

        **Lists**
        ```markdown
        - Item 1
        - Item 2

        1. First
        2. Second
        ```

        **Links**
        ```markdown
        [Link Text](URL)
        ```
        """)

    with col2:
        st.markdown("""
        **Code**
        ```markdown
        `inline code`

        ```python
        code block
        ```
        ```

        **Blockquote**
        ```markdown
        > This is a quote
        ```

        **Table**
        ```markdown
        | Header | Header |
        |--------|--------|
        | Cell   | Cell   |
        ```

        **Horizontal Rule**
        ```markdown
        ---
        ```
        """)

st.caption("Markdown Editor - Built with Streamlit")
