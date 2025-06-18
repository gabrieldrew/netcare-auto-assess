import streamlit as st

from assessment.assessor import assess_claim
from ocr.pdf_reader import extract_text_from_pdf
from parsing.statement_parser import parse_statement
from retrieval.vector_search import load_policy_index, retrieve_rules

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

if st.button("Run pre‑assessment") and claim_pdf and provider_pdf:
    with st.spinner("Processing…"):
        claim_text = extract_text_from_pdf(claim_pdf)
        provider_text = extract_text_from_pdf(provider_pdf)
        claim_struct = parse_statement(claim_text + "\n" + provider_text)
        rules = retrieve_rules(st.session_state.policy_index, claim_struct)
        result = assess_claim(claim_struct, rules)
    st.subheader("Pre‑assessment result")
    st.json(result)
    st.markdown(":warning: **Demo only – human audit required before payment.**")
