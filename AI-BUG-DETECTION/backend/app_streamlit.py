import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Add parent path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.static_analyzer import StaticAnalyzer
from services.ai_analyzer import AIAnalyzer
from services.result_fusion import ResultFusion
from services.validation_service import ValidationService

# Set Streamlit Page Config
st.set_page_config(
    page_title="AI Bug Detection - Playground",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium developer styling
st.markdown("""
<style>
    .reportview-container {
        background-color: #0b0c10;
        color: #e3e6ed;
    }
    .stButton>button {
        background-color: #1f2833;
        color: #66fcf1;
        border: 1px solid #45a29e;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #66fcf1;
        color: #0b0c10;
        border-color: #66fcf1;
    }
    .severity-badge {
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 11px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Services
@st.cache_resource
def get_services():
    return StaticAnalyzer(), AIAnalyzer(), ResultFusion(), ValidationService()

static_analyzer, ai_analyzer, result_fusion, validation_service = get_services()

# Sidebar Setup
st.sidebar.title("🛡️ AI Bug Detection")
st.sidebar.markdown("---")

language = st.sidebar.selectbox("Target Language", ["Python", "JavaScript"])
sample_option = st.sidebar.selectbox(
    "Load Sample Code",
    ["None (Blank)", "Division by Zero", "SQL Injection", "Missing Input Validation"]
)

# Load Sample Code Content
SAMPLE_CODES = {
    "Division by Zero": """def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

result = calculate_average([])
print(result)
""",
    "SQL Injection": """import sqlite3

def get_user_profile(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Bug: SQL injection pattern via string formatting
    query = "SELECT * FROM users WHERE username = '%s'" % username
    cursor.execute(query)
    return cursor.fetchall()
""",
    "Missing Input Validation": """def process_withdrawal(account_balance, amount):
    # Bug: Missing input validation for negative transfer amount
    account_balance -= amount
    return account_balance
"""
}

default_code = SAMPLE_CODES.get(sample_option, "")

# Layout Setup
st.title("AI Bug Detection & Remediation Playground")
st.subheader("Analyze code using combined Static analysis & LangChain/OpenAI reasoning.")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### Code Workspace")
    file_name = st.text_input("Filename", "sample_code.py" if language == "Python" else "sample_code.js")
    
    # Show editor
    code_input = st.text_area("Source Code", default_code, height=350, placeholder="Paste your buggy code here...")
    
    analyze_btn = st.button("Run Bug Analysis Pipeline", use_container_width=True)

# Session state to store analysis results
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if analyze_btn:
    if not code_input.strip():
        st.warning("Please provide code to analyze.")
    else:
        with st.spinner("Executing Pipeline (AST Checks, AI reasoning, Classification)..."):
            # Execute Static
            static_res = static_analyzer.analyze(language, code_input, file_name)
            # Execute AI
            ai_res = ai_analyzer.analyze_code(language, code_input, file_name)
            # Fuse
            fused_bugs = result_fusion.fuse(static_res, ai_res)
            
            st.session_state.analysis_results = {
                "bugs": fused_bugs,
                "code": code_input
            }

with col2:
    st.markdown("### Analysis Results")
    
    if st.session_state.analysis_results is None:
        st.info("Run the analysis pipeline on the left workspace to inspect bugs.")
    else:
        bugs = st.session_state.analysis_results["bugs"]
        if not bugs:
            st.success("✓ No bugs detected by AST or LLM analyzer engines.")
        else:
            st.warning(f"Found {len(bugs)} potential bugs.")
            
            # Show list of bugs in tabs or selectbox
            bug_options = [f"{b['id'] if 'id' in b else 'BUG'}: {b['type']} (Line {b['line']})" for b in bugs]
            selected_bug_idx = st.selectbox("Select a Bug to Inspect", range(len(bugs)), format_func=lambda i: bug_options[i])
            
            selected_bug = bugs[selected_bug_idx]
            
            # Render Bug Details Card
            st.markdown(f"#### {selected_bug['type']} ({selected_bug.get('bug_id', 'BUG-001')})")
            
            # Severity color helpers
            sev = selected_bug['severity'].upper()
            sev_colors = {"CRITICAL": "#ef4444", "HIGH": "#f97316", "MEDIUM": "#eab308", "LOW": "#22c55e"}
            st.markdown(
                f'<span style="background-color: {sev_colors.get(sev, "#888")}15; color: {sev_colors.get(sev, "#888")}; '
                f'border: 1px solid {sev_colors.get(sev, "#888")}30; padding: 4px 8px; border-radius: 4px; '
                f'font-size: 12px; font-weight: bold;">SEVERITY: {sev}</span>'
                f' &nbsp; &nbsp; <span style="font-size:12px; color:#888;">AI Confidence Score: **{int(selected_bug.get("confidence", 0.9) * 100)}%**</span>',
                unsafe_allow_html=True
            )
            
            st.markdown(f"**Location**: `{selected_bug.get('file')}` on **Line {selected_bug.get('line')}**")
            st.markdown(f"**Description**: {selected_bug.get('description')}")
            
            # Accordions for details
            with st.expander("Root Cause Explanation", expanded=True):
                st.write(selected_bug.get("explanation"))
            with st.expander("Potential Runtime Impact"):
                st.write(selected_bug.get("impact"))
            with st.expander("Fix Recommendation"):
                st.write(selected_bug.get("suggestion"))
                
            # Remediation workspace
            st.markdown("---")
            st.markdown("### Remediation Workspace")
            
            # Show Side-by-Side original vs fix code
            original = st.session_state.analysis_results["code"]
            fixed_proposal = selected_bug.get("fixed_code") or original
            
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                st.markdown("**Original**")
                st.code(original, language=language.lower())
            with subcol2:
                st.markdown("**Proposed Fix**")
                st.code(fixed_proposal, language=language.lower())
                
            if st.button("Validate Proposed Fix"):
                with st.spinner("Running syntax gates & mock compiler tests..."):
                    val_res = validation_service.validate(
                        language,
                        original,
                        fixed_proposal,
                        selected_bug.get("test_case") or ""
                    )
                    
                    st.markdown("#### Validation Output")
                    st.write(f"Syntax Validation: {'✓' if val_res['syntax_check'] else '✗'}")
                    st.write(f"Static Analysis Checks: {'✓' if val_res['static_analysis'] else '✗'}")
                    st.write(f"Unit Test Run: {'✓' if val_res['test_run'] else '✗'}")
                    
                    if val_res['passed']:
                        st.success("🎉 BUG RESOLVED SUCCESSFULLY!")
                    else:
                        st.error("❌ VALIDATION FAILED")
