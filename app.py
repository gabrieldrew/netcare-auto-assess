import streamlit as st
import base64
from datetime import datetime

from assessment.assessor import assess_claim
from ocr.pdf_reader import extract_text_from_pdf
from parsing.claim_form_ai import ai_extract
from parsing.statement_parser import parse_statement
from retrieval.vector_search import load_policy_index, retrieve_rules
from utils.pdf_generator import generate_assessment_pdf


def load_css():
    """Load custom CSS styling."""
    
    # Load custom style.css
    try:
        with open('style.css', 'r') as f:
            custom_css = f.read()
        st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("style.css file not found.")


def display_header():
    """Display professional header."""
    # Load logo
    try:
        with open("netcarelogo.png", "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_data}" alt="Netcare Plus Logo" style="width: 64px; height: 64px; object-fit: contain;" />'
    except FileNotFoundError:
        logo_html = '''
        <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #22D3EE, #0891B2, #22D3EE); border-radius: 14px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 24px; box-shadow: 0 8px 24px rgba(34, 211, 238, 0.4);">
            N+
        </div>
        '''
    
    st.markdown(f"""
    <div class="netcare-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="logo">
                    {logo_html}
                </div>
                <div class="brand-info">
                    <h1>NetcarePlus</h1>
                    <p>GapCare Assessment Platform</p>
                </div>
            </div>
            <div class="header-actions">
                <div class="demo-badge">
                    <div class="status-indicator"></div>
                    Demo Environment
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_hero_section():
    """Display hero section."""
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h1>GapCare Claim Pre-Assessment</h1>
            <p>Intelligent claim processing with automated policy rule application and instant assessment results</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_upload_section():
    """Display document upload section."""
    st.markdown("""
    <div class="upload-section">
        <div class="upload-intro">
            <h2>Document Upload</h2>
            <p>Please upload all required documents to process your GapCare claim assessment. All documents must be in PDF format.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create three columns for upload cards
    col1, col2, col3 = st.columns(3, gap="large")
    
    files = {}
    
    with col1:
        st.markdown("""
        <div class="upload-card">
            <div class="upload-card-header">
                <div class="upload-card-icon">
                    <svg width="24" height="24" fill="#22D3EE" viewBox="0 0 24 24">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>
                        <path d="M14 2v6h6"/>
                        <path d="M16 13H8"/>
                        <path d="M16 17H8"/>
                        <path d="M10 9H8"/>
                    </svg>
                </div>
                <h3>Medical Scheme Statement</h3>
                <p>Upload your medical aid statement PDF showing the claim details and any payments made by your scheme.</p>
            </div>
        """, unsafe_allow_html=True)
        
        files['medical'] = st.file_uploader(
            "Medical Scheme Statement",
            type=["pdf"],
            key="medical_statement",
            label_visibility="collapsed"
        )
        
        if files['medical']:
            st.markdown('<div class="upload-success">✓ File uploaded successfully</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="upload-card">
            <div class="upload-card-header">
                <div class="upload-card-icon">
                    <svg width="24" height="24" fill="#22D3EE" viewBox="0 0 24 24">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>
                        <path d="M14 2v6h6"/>
                        <path d="M9 15l2 2 4-4"/>
                    </svg>
                </div>
                <h3>Provider Invoice</h3>
                <p>Upload your healthcare provider invoice showing the full amount charged for medical services received.</p>
            </div>
        """, unsafe_allow_html=True)
        
        files['provider'] = st.file_uploader(
            "Provider Invoice",
            type=["pdf"],
            key="provider_invoice",
            label_visibility="collapsed"
        )
        
        if files['provider']:
            st.markdown('<div class="upload-success">✓ File uploaded successfully</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="upload-card">
            <div class="upload-card-header">
                <div class="upload-card-icon">
                    <svg width="24" height="24" fill="#22D3EE" viewBox="0 0 24 24">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>
                        <path d="M14 2v6h6"/>
                        <path d="M12 18h.01"/>
                        <path d="M12 6v8"/>
                    </svg>
                </div>
                <h3>GapCover Claim Form</h3>
                <p>Upload your completed GapCare claim form with all required information and signatures.</p>
            </div>
        """, unsafe_allow_html=True)
        
        files['claim'] = st.file_uploader(
            "GapCover Claim Form",
            type=["pdf"],
            key="claim_form",
            label_visibility="collapsed"
        )
        
        if files['claim']:
            st.markdown('<div class="upload-success">✓ File uploaded successfully</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    return files['medical'], files['provider'], files['claim']


def display_process_button(all_files_uploaded):
    """Display process button."""
    st.markdown('<div class="process-section">', unsafe_allow_html=True)
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    
    if not all_files_uploaded:
        st.markdown('<p class="help-text">Please upload all three documents to enable assessment</p>', unsafe_allow_html=True)
    
    clicked = st.button(
        "Run Pre-Assessment",
        disabled=not all_files_uploaded,
        type="primary",
        use_container_width=True
    )
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    return clicked


def display_processing_status():
    """Display processing animation."""
    st.markdown("""
    <div class="processing-card">
        <div class="processing-content">
            <div class="processing-spinner"></div>
            <h3>Processing Your Claim</h3>
            <p>Analyzing documents and applying policy rules...</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_assessment_result(result, claim_data, claim_form_data):
    """Display assessment result."""
    st.markdown('<div class="results-section">', unsafe_allow_html=True)
    
    # Main result card
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    # Header with status
    status_class = "status-covered" if result["covered"] else "status-declined"
    status_text = "CLAIM APPROVED" if result["covered"] else "CLAIM DECLINED"
    
    st.markdown(f"""
    <div class="result-header">
        <h2>Assessment Result</h2>
        <div class="status-badge {status_class}">
            {status_text}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Applicable benefits
    if result["benefits"]:
        st.markdown("""
        <div class="result-section">
            <h3>Applicable Benefits</h3>
        """, unsafe_allow_html=True)
        
        for benefit in result["benefits"]:
            st.markdown(f"""
            <div class="benefit-item">
                <span>• {benefit}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Payable amount
    if result["payable_amount_ZAR"]:
        st.markdown(f"""
        <div class="result-section">
            <h3>Financial Assessment</h3>
            <div class="financial-highlight">
                <p>Estimated Payable Amount: {result["payable_amount_ZAR"]}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Explanation
    st.markdown(f"""
    <div class="result-section">
        <h3>Assessment Details</h3>
        <div class="explanation-box">
            <p>{result["explanation"]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close result card
    
    # PDF Download section
    st.markdown("""
    <div class="download-card">
        <h3>Download Assessment Report</h3>
    """, unsafe_allow_html=True)
    
    # Generate PDF
    pdf_buffer = generate_assessment_pdf(claim_data, result, claim_form_data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"GapCare_Assessment_{timestamp}.pdf"
    
    st.download_button(
        label="Download Comprehensive PDF Report",
        data=pdf_buffer.getvalue(),
        file_name=filename,
        mime="application/pdf",
        use_container_width=True
    )
    
    st.markdown('<p class="help-text">Download a detailed PDF report of this assessment for your records</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # Close download card
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close results section


def display_technical_details(claim_data, claim_form_data, result):
    """Display technical details."""
    st.markdown('<div class="technical-section">', unsafe_allow_html=True)
    
    with st.expander("Technical Details & Raw Data", expanded=False):
        tab1, tab2, tab3 = st.tabs(["📊 Extracted Claim Data", "📝 Claim Form Fields", "🔍 Assessment Result"])
        
        with tab1:
            st.json(claim_data)
        
        with tab2:
            st.json(claim_form_data)
        
        with tab3:
            st.json(result)
    
    st.markdown('</div>', unsafe_allow_html=True)


def display_disclaimer():
    """Display disclaimer."""
    st.markdown("""
    <div class="disclaimer-section">
        <div class="disclaimer-card">
            <div class="disclaimer-content">
                <svg class="disclaimer-icon" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                </svg>
                <div class="disclaimer-text">
                    <h4>Important Notice</h4>
                    <p>This is a demonstration system for testing purposes only. All assessments require human verification and approval before any payment processing occurs. Results shown are for demonstration purposes and should not be considered as final claim decisions.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application function."""
    
    # Configure page
    st.set_page_config(
        page_title="NetcarePlus GapCare Assessment",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Load custom CSS
    load_css()
    
    # Main background container using globals.css
    st.markdown('<div class="bg-netcare-gradient-enhanced min-h-screen">', unsafe_allow_html=True)
    
    # Display header
    display_header()
    
    # Display hero section
    display_hero_section()
    
    # Load policy index
    if "policy_index" not in st.session_state:
        with st.spinner("Loading policy index..."):
            try:
                st.session_state.policy_index = load_policy_index()
                st.success("✅ Policy index loaded successfully")
            except Exception as e:
                st.error(f"❌ Policy index missing: {e}")
                st.stop()
    
    # Display upload section
    medical_pdf, provider_pdf, claim_pdf = display_upload_section()
    
    # Process button
    all_files_uploaded = all([medical_pdf, provider_pdf, claim_pdf])
    button_clicked = display_process_button(all_files_uploaded)
    
    # Processing logic
    if button_clicked and all_files_uploaded:
        processing_placeholder = st.empty()
        
        with processing_placeholder:
            display_processing_status()
        
        try:
            # Process documents
            medical_statement_text = extract_text_from_pdf(medical_pdf)
            provider_statement_text = extract_text_from_pdf(provider_pdf)
            claim_form_text = extract_text_from_pdf(claim_pdf)
            
            medical_statement_data = parse_statement(medical_statement_text)
            provider_statement_data = parse_statement(provider_statement_text)
            claim_form_data = ai_extract(claim_form_text)
            
            claim_data = {
                "medical_aid_statement": medical_statement_data,
                "provider_statement": provider_statement_data,
                **claim_form_data,
            }
            
            rules = retrieve_rules(st.session_state.policy_index, claim_data)
            result = assess_claim(claim_data, rules)
            
            # Clear processing status
            processing_placeholder.empty()
            
            # Display results
            display_assessment_result(result, claim_data, claim_form_data)
            
            # Technical details
            display_technical_details(claim_data, claim_form_data, result)
            
            # Disclaimer
            display_disclaimer()
            
        except Exception as e:
            processing_placeholder.empty()
            st.error(f"❌ An error occurred during processing: {str(e)}")
    
    # Close background container
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()