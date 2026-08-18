import streamlit as st

st.set_page_config(page_title="Bugs List", page_icon="🛡️", layout="wide")

st.title("🛡️ Detected Bugs List")
st.markdown("Inspect details, explanations, and safety recommendations for each detected flaw.")

# Check if analysis exists
if "latest_bugs" not in st.session_state or not st.session_state.latest_bugs:
    st.info("No bugs loaded in workspace. Please run a fresh pipeline on the **1_Code_Analysis** page first.")
else:
    bugs = st.session_state.latest_bugs
    
    # Severity Filter
    severity_filter = st.selectbox("Severity Classification Filter", ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
    
    filtered_bugs = [
        b for b in bugs 
        if severity_filter == "ALL" or b["severity"].upper() == severity_filter.upper()
    ]
    
    if not filtered_bugs:
        st.success("No flaws match the active severity filters.")
    else:
        st.markdown(f"Displaying {len(filtered_bugs)} bugs:")
        
        # Display each bug in a structured layout
        for idx, bug in enumerate(filtered_bugs):
            with st.container():
                st.markdown(f"### {bug['type']} &nbsp; `({bug.get('bug_id', 'BUG-' + str(idx+1))})`", unsafe_allow_html=True)
                
                # Badges
                sev = bug['severity'].upper()
                sev_colors = {"CRITICAL": "#ef4444", "HIGH": "#f97316", "MEDIUM": "#eab308", "LOW": "#22c55e"}
                st.markdown(
                    f'<span style="background-color: {sev_colors.get(sev, "#888")}15; color: {sev_colors.get(sev, "#888")}; '
                    f'border: 1px solid {sev_colors.get(sev, "#888")}30; padding: 4px 8px; border-radius: 4px; '
                    f'font-size: 11px; font-weight: bold;">SEVERITY: {sev}</span>'
                    f' &nbsp; &nbsp; <span style="font-size:11px; color:#888;">AI Confidence Score: **{int(bug.get("confidence", 0.9) * 100)}%**</span>'
                    f' &nbsp; &nbsp; <span style="font-size:11px; color:#888;">File: `{bug.get("file")}:{bug.get("line")}`</span>',
                    unsafe_allow_html=True
                )
                
                st.markdown(f"**Description**: {bug.get('description')}")
                
                # Split columns for details
                det_col1, det_col2 = st.columns(2)
                with det_col1:
                    st.info(f"**Explanation**:\n{bug.get('explanation')}")
                with det_col2:
                    st.warning(f"**Impact Assessment**:\n{bug.get('impact')}")
                    
                st.write(f"**Remediation Suggestion**: {bug.get('suggestion')}")
                
                # CTA button to select for fixing
                if st.button(f"Load Bug {bug.get('bug_id', 'BUG-' + str(idx+1))} into Remediation Studio", key=f"remed_{idx}"):
                    st.session_state.selected_bug = bug
                    st.success(f"✓ {bug.get('bug_id', 'BUG-' + str(idx+1))} loaded! Open the **3_Remediation_Studio** subpage to perform fix actions.")
                
                st.markdown("---")
