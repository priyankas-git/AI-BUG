import streamlit as st
import os
import sys

# Appending backend path for service access
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
sys.path.append(backend_path)

from services.fix_generator import FixGenerator
from services.validation_service import ValidationService

st.set_page_config(page_title="Remediation Studio", page_icon="🔧", layout="wide")

st.title("🔧 Remediation Studio")
st.markdown("Compare code versions side-by-side and execute the automated verification pipeline to validate fixes.")

# Check if a bug is loaded
if "selected_bug" not in st.session_state or not st.session_state.selected_bug:
    st.info("No active bug selected. Please visit the **2_Bugs_List** page and select a bug to load it here.")
else:
    bug = st.session_state.selected_bug
    original_code = st.session_state.get("original_code", "")
    language = st.session_state.get("selected_language", "Python")
    
    st.markdown(f"### Remediating: {bug['type']} `({bug.get('bug_id', 'BUG-001')})`", unsafe_allow_html=True)
    st.write(f"**Vulnerability File/Line**: `{bug.get('file')}:{bug.get('line')}`")
    
    # Active Workspace Setup
    if "custom_fixed_code" not in st.session_state:
        st.session_state.custom_fixed_code = bug.get("fixed_code") or original_code
        
    # Actions
    act_col1, act_col2, act_col3 = st.columns(3)
    
    with act_col1:
        if st.button("Regenerate AI Fix"):
            with st.spinner("Invoking LLM fix engine via LangChain..."):
                try:
                    fix_gen = FixGenerator()
                    response = fix_gen.generate_fix(language, original_code, bug)
                    st.session_state.custom_fixed_code = response["fixed_code"]
                    st.success("✓ AI suggested code generated!")
                except Exception as e:
                    st.error(f"Error calling fix generator: {str(e)}")
                    
    with act_col2:
        applied_btn = st.button("Apply Fix Changes")
        if applied_btn:
            st.success("✓ Changes marked as applied locally.")
            
    with act_col3:
        validate_btn = st.button("Run Verification Pipeline", type="primary")

    # Code Diff side-by-side
    st.markdown("---")
    edit_col1, edit_col2 = st.columns(2)
    
    with edit_col1:
        st.markdown("**Original Buggy Code**")
        st.code(original_code, language=language.lower())
        
    with edit_col2:
        st.markdown("**Corrected Code Block**")
        # Let developer edit code directly in text area if they want to tune the fix
        new_fixed_code = st.text_area(
            "Modify Corrected Code",
            st.session_state.custom_fixed_code,
            height=250,
            label_visibility="collapsed"
        )
        st.session_state.custom_fixed_code = new_fixed_code

    # Run verification pipeline
    if validate_btn:
        st.markdown("---")
        st.markdown("### Pipeline Verification Logs")
        
        with st.spinner("Executing compilations, AST verification, and unit assertions..."):
            try:
                validator = ValidationService()
                val_res = validator.validate(
                    language,
                    original_code,
                    st.session_state.custom_fixed_code,
                    bug.get("test_case") or ""
                )
                
                # Render results checklist
                chk1, chk2, chk3, chk4 = st.columns(4)
                with chk1:
                    st.markdown(f"**Syntax Validation**: {'🟢 PASS' if val_res['syntax_check'] else '🔴 FAIL'}")
                with chk2:
                    st.markdown(f"**Static Analysis**: {'🟢 PASS' if val_res['static_analysis'] else '🔴 FAIL'}")
                with chk3:
                    st.markdown(f"**Test Generation**: {'🟢 PASS' if val_res['test_run'] else '🔴 FAIL'}")
                with chk4:
                    st.markdown(f"**Unit Assertions**: {'🟢 PASS' if val_res['passed'] else '🔴 FAIL'}")
                    
                st.markdown("---")
                if val_res['passed']:
                    st.success("🎉 BUG RESOLVED SUCCESSFULLY!")
                    
                    # Update status in local storage/session state
                    if "latest_bugs" in st.session_state:
                        for b in st.session_state.latest_bugs:
                            if b.get("bug_id") == bug.get("bug_id"):
                                b["status"] = "RESOLVED"
                else:
                    st.error("❌ VALIDATION FAILED. Review code syntax or assertions.")
                    
            except Exception as e:
                st.error(f"Error executing validation pipeline: {str(e)}")
                
    # Show associated test case if available
    if bug.get("test_case"):
        with st.expander("Inspection Test Code Details"):
            st.code(bug.get("test_case"), language="python" if language == "Python" else "javascript")
