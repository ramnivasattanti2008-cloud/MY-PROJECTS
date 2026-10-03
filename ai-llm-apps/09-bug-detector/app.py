"""
Bug Detector - Find and fix bugs in Python code
Uses Gemini AI for intelligent code analysis
"""

import streamlit as st
import os
import google.generativeai as genai
import re

# Page configuration
st.set_page_config(
    page_title="Bug Detector",
    page_icon="🐛",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #EF4444; }
    .sub-header { font-size: 1.2rem; color: #F87171; }
    .bug-box { background-color: #1E1E2E; padding: 15px; border-radius: 10px; border-left: 4px solid #EF4444; }
    .fix-box { background-color: #1E1E2E; padding: 15px; border-radius: 10px; border-left: 4px solid #10B981; }
    .explanation { background-color: #1a1a2e; padding: 15px; border-radius: 10px; border-left: 4px solid #3B82F6; }
    .stTextArea > div > div > textarea { background-color: #1E1E2E; }
</style>
""", unsafe_allow_html=True)

def get_gemini_api_key(api_key_input: str = None) -> str:
    """Get Gemini API key from various sources"""
    if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
        return st.secrets['GEMINI_API_KEY']
    if os.environ.get('GEMINI_API_KEY'):
        return os.environ.get('GEMINI_API_KEY')
    if api_key_input:
        return api_key_input
    return None

def setup_gemini(api_key: str):
    """Configure Gemini with API key"""
    if api_key:
        genai.configure(api_key=api_key)

def analyze_code(code: str, model) -> dict:
    """Analyze code for bugs and provide fixes"""
    prompt = f"""Analyze the following Python code for bugs, errors, and potential issues.
Provide a detailed analysis with:
1. Identified bugs/issues
2. Explanation of what's wrong
3. Corrected code
4. Best practices tips

Format your response with clear sections.

Code:
```{code}
```"""

    try:
        response = model.generate_content(prompt)
        return parse_analysis(response.text)
    except Exception as e:
        return {"error": str(e)}

def parse_analysis(text: str) -> dict:
    """Parse Gemini's analysis into structured format"""
    result = {
        "bugs": [],
        "explanation": "",
        "fixed_code": "",
        "tips": []
    }

    lines = text.split('\n')
    current_section = None
    section_content = []

    for line in lines:
        line = line.strip()

        if 'bug' in line.lower() or 'issue' in line.lower() or 'problem' in line.lower():
            if section_content:
                if current_section == 'bugs':
                    result['bugs'].extend(section_content)
                elif current_section == 'explanation':
                    result['explanation'] = '\n'.join(section_content)
                elif current_section == 'tips':
                    result['tips'].extend(section_content)
            current_section = 'bugs'
            section_content = []
        elif line.startswith('Explanation') or line.startswith('What\'s wrong'):
            if section_content and current_section == 'bugs':
                result['bugs'].extend(section_content)
            current_section = 'explanation'
            section_content = []
        elif 'fixed' in line.lower() or 'corrected' in line.lower() or '```python' in line.lower():
            if section_content and current_section == 'explanation':
                result['explanation'] = '\n'.join(section_content)
            current_section = 'fixed'
            section_content = []
        elif 'tip' in line.lower() or 'best practice' in line.lower() or 'suggestion' in line.lower():
            if section_content and current_section == 'fixed':
                result['fixed_code'] = '\n'.join(section_content)
            current_section = 'tips'
            section_content = []
        elif line and current_section:
            section_content.append(line)

    # Capture remaining content
    if current_section == 'bugs' and section_content:
        result['bugs'].extend(section_content)
    elif current_section == 'explanation' and section_content:
        result['explanation'] = '\n'.join(section_content)
    elif current_section == 'fixed' and section_content:
        result['fixed_code'] = '\n'.join(section_content)
    elif current_section == 'tips' and section_content:
        result['tips'].extend(section_content)

    # If no structured parsing worked, use raw text
    if not result['bugs'] and not result['explanation']:
        result['explanation'] = text

    return result

def main():
    # Header
    st.markdown('<p class="main-header">🐛 Bug Detector</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Find and fix bugs in your Python code</p>', unsafe_allow_html=True)
    st.divider()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        api_key_input = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get your API key from Google AI Studio"
        )

        st.markdown("---")
        st.markdown("""
        **What it detects:**
        - Syntax errors
        - Logic bugs
        - Runtime exceptions
        - Best practice violations
        - Security issues
        """)

        st.markdown("---")
        st.markdown("**Supported Languages:**")
        st.markdown("- Python (primary)")
        st.markdown("- JavaScript")
        st.markdown("- Other languages via analysis")

    # Main content
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("💻 Paste Your Code")

        code = st.text_area(
            "Python Code",
            placeholder="""# Example buggy code:
def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

result = calculate_average([])
print(result)""",
            height=300
        )

        language = st.selectbox("Language", ["Python", "JavaScript", "Other"])

        analyze_btn = st.button("🔍 Find Bugs", type="primary", use_container_width=True)

        # Quick paste examples
        st.markdown("**Quick Examples:**")
        example = st.button("Fill with buggy example", use_container_width=True)

        if example:
            st.session_state['example_code'] = '''# Buggy code example
def find_max(numbers):
    max = numbers[0]
    for i in numbers:
        if i > max:
            max = i
    return max

# Bug: what if list is empty?
print(find_max([]))'''

    # Results
    if analyze_btn and code:
        api_key = get_gemini_api_key(api_key_input)

        if not api_key:
            st.error("⚠️ Please enter your Gemini API key in the sidebar!")
        else:
            with st.spinner("Analyzing code..."):
                try:
                    setup_gemini(api_key)
                    model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    analysis = analyze_code(code, model)

                    if "error" in analysis:
                        st.error(analysis["error"])
                    else:
                        # Show explanation
                        if analysis["explanation"]:
                            st.markdown("### 📖 Analysis")
                            st.markdown(f'<div class="explanation">{analysis["explanation"]}</div>', unsafe_allow_html=True)

                        # Show bugs
                        if analysis["bugs"]:
                            st.markdown("### 🐛 Issues Found")
                            for bug in analysis["bugs"]:
                                if bug.strip():
                                    st.markdown(f'<div class="bug-box">⚠️ {bug}</div>', unsafe_allow_html=True)

                        # Show fixed code
                        if analysis["fixed_code"]:
                            st.markdown("### ✅ Fixed Code")
                            st.code(analysis["fixed_code"], language="python")

                        # Show tips
                        if analysis["tips"]:
                            st.markdown("### 💡 Best Practices")
                            for tip in analysis["tips"]:
                                if tip.strip():
                                    st.success(tip)

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Features section
    st.divider()
    st.subheader("✨ Features")

    features = st.columns(3)
    with features[0]:
        st.info("**🐛 Bug Detection**\n\nIdentifies syntax errors, logic bugs, and runtime exceptions")
    with features[1]:
        st.info("**🔧 Auto Fix**\n\nProvides corrected code with explanations")
    with features[2]:
        st.info("**📚 Learning**\n\nExplains why code is buggy and best practices")

if __name__ == "__main__":
    main()
