import streamlit as st

from assessment.assessor import assess_claim
from ocr.pdf_reader import extract_text_from_pdf
from parsing.statement_parser import parse_statement
from parsing.claim_form_ai import ai_extract
from retrieval.vector_search import load_policy_index, retrieve_rules

def display_assessment_result(result):
    """Display the assessment result in a user-friendly format."""
    
    # Coverage status with color coding
    if result["covered"]:
        st.success("✅ **CLAIM COVERED**")
    else:
        st.error("❌ **CLAIM NOT COVERED**")
    
    # Applicable benefits
    if result["benefits"]:
        st.subheader("📋 Applicable Benefits")
        for benefit in result["benefits"]:
            st.write(f"• **{benefit}**")
    else:
        st.write("**No applicable benefits found**")
    
    # Payable amount
    st.subheader("💰 Assessment")
    if result["payable_amount_ZAR"]:
        st.write(f"**Estimated Payable Amount:** {result['payable_amount_ZAR']}")
    else:
        st.write("**Payable Amount:** Not applicable")
    
    # Detailed explanation
    st.subheader("📝 Explanation")
    st.write(result["explanation"])

st.title("GapCare Claim Pre‑Assessor (Demo)")

# Load policy index lazily to keep app startup snappy
if "policy_index" not in st.session_state:
    try:
        st.session_state.policy_index = load_policy_index()
        st.success("Policy index loaded.")
    except Exception as e:
        st.error(f"Policy index missing: {e}")

claim_pdf = st.file_uploader("Medical Scheme Statement PDF", type=["pdf"])
provider_pdf = st.file_uploader("Provider Invoice PDF", type=["pdf"])
claim_form_pdf = st.file_uploader("GapCover Claim Form PDF", type=["pdf"])

if st.button("Run pre‑assessment") and claim_pdf and provider_pdf and claim_form_pdf:
    with st.spinner("Processing…"):
        claim_text = extract_text_from_pdf(claim_pdf)
        provider_text = extract_text_from_pdf(provider_pdf)
        claim_form_text = extract_text_from_pdf(claim_form_pdf)
        claim_struct = parse_statement(claim_text + "\n" + provider_text)
        claim_meta = ai_extract(claim_form_text)
        claim_struct.update(claim_meta)
        rules = retrieve_rules(st.session_state.policy_index, claim_struct)
        result = assess_claim(claim_struct, rules)
    
    st.subheader("Pre‑assessment Result")
    display_assessment_result(result)
    
    # Show raw data in an expander for technical users
    with st.expander("Technical Details"):
        st.write("**Extracted Claim Data:**")
        st.json(claim_struct)
        st.write("**Claim Form Fields:**")
        st.json(claim_meta)
        st.write("**Raw Assessment Result:**")
        st.json(result)
    
    st.markdown(":warning: **Demo only – human audit required before payment.**")
