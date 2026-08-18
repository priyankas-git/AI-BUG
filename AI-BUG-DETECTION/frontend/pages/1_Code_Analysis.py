import streamlit as st
import os
import sys
import time

# Appending backend path for service access
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
sys.path.append(backend_path)

from services.static_analyzer import StaticAnalyzer
from services.ai_analyzer import AIAnalyzer
from services.result_fusion import ResultFusion

st.set_page_config(page_title="Code Analysis", page_icon="💻", layout="wide")

st.title("💻 Code Analysis Workspace")
st.markdown("Analyze submitted source code using deterministic static parser AST tools combined with LLM engines.")

# Sample codes setup
SAMPLE_CODES = {
    "Python: Division by Zero": """def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

result = calculate_average([])
print(result)
""",
    "Python: SQL Injection": """import sqlite3

def get_user_profile(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Bug: SQL injection pattern via string formatting
    query = "SELECT * FROM users WHERE username = '%s'" % username
    cursor.execute(query)
    return cursor.fetchall()
""",
    "JavaScript: Null Reference Access": """function processUser(user) {
  console.log("Processing user: " + user.name);
  let email = user.address.email; // Potential null access crash
  return email;
}

processUser(null);
"""
}

# Controls layout
col1, col2 = st.columns([1, 2])
with col1:
    language = st.selectbox("Language Selector", ["Python", "JavaScript"])
    sample_select = st.selectbox("Pre-load Buggy Samples", ["Blank Workspace"] + list(SAMPLE_CODES.keys()))
    file_name = st.text_input("Analysis File Target", "example.py" if language == "Python" else "example.js")

default_code = SAMPLE_CODES.get(sample_select, "")

# Editor Area
code_body = st.text_area("Source Code Workspace", default_code, height=350)

# Run pipeline
if st.button("Run Code Analysis Engine", use_container_width=True):
    if not code_body.strip():
        st.warning("Workspace empty. Please enter or paste target code.")
    else:
        # Pipeline execution logs UI
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            ("Parsing code", 15),
            ("Static analysis", 30),
            ("AI reasoning", 50),
            ("Bug classification", 70),
            ("Severity assessment", 85),
            ("Fix generation", 100)
        ]
        
        for text, percent in steps:
            status_text.markdown(f"**Analyzing...** ✓ {text}")
            progress_bar.progress(percent)
            time.sleep(0.2)
            
        try:
            # Instantiate services
            static_ana = StaticAnalyzer()
            ai_ana = AIAnalyzer()
            fusion = ResultFusion()
            
            # Execute Pipeline
            static_res = static_ana.analyze(language, code_body, file_name)
            ai_res = ai_ana.analyze_code(language, code_body, file_name)
            fused_bugs = fusion.fuse(static_res, ai_res)
            
            # Update Session State
            st.session_state.latest_bugs = fused_bugs
            st.session_state.original_code = code_body
            st.session_state.selected_language = language
            st.session_state.selected_file = file_name
            
            # Show summary
            st.success(f"✓ Analysis complete! Found {len(fused_bugs)} flaws.")
            
            # Severity counters
            counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
            for b in fused_bugs:
                sev = b["severity"].upper()
                if sev in counts:
                    counts[sev] += 1
                    
            st.markdown("#### Detected Bugs Summary")
            st.markdown(
                f"- **Critical**: `{counts['CRITICAL']}` &nbsp; "
                f"- **High**: `{counts['HIGH']}` &nbsp; "
                f"- **Medium**: `{counts['MEDIUM']}` &nbsp; "
                f"- **Low**: `{counts['LOW']}`"
            )
            
            st.info("Navigate to the **2_Bugs_List** subpage in the sidebar to inspect detailed reports.")
            
        except Exception as e:
            st.error(f"Execution error running analysis pipeline: {str(e)}")
