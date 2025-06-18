import { useState } from 'react';

export default function Home() {
  const [medical, setMedical] = useState(null);
  const [provider, setProvider] = useState(null);
  const [claim, setClaim] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [dragActive, setDragActive] = useState(null);

  const allUploaded = medical && provider && claim;

  const handleSubmit = async () => {
    if (!allUploaded) return;
    const formData = new FormData();
    formData.append('medical', medical);
    formData.append('provider', provider);
    formData.append('claim', claim);

    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/assess', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();

      if (!res.ok || !data.result) {
        throw new Error(data.detail || 'Invalid response from server');
      }

      setResult(data);
    } catch (error) {
      console.error('Assessment failed:', error);
      alert('Assessment failed. Please try again.');
      setResult(null);
    }
    setLoading(false);
  };

  const handleDrag = (e, fileType) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(fileType);
    } else if (e.type === "dragleave") {
      setDragActive(null);
    }
  };

  const handleDrop = (e, setter) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(null);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      setter(files[0]);
    }
  };

  const FileUploadArea = ({ file, setter, label, description, fileType, icon }) => (
    <div className="upload-container">
      <div 
        className={`file-drop-zone ${dragActive === fileType ? 'drag-active' : ''} ${file ? 'file-uploaded' : ''}`}
        onDragEnter={(e) => handleDrag(e, fileType)}
        onDragLeave={(e) => handleDrag(e, fileType)}
        onDragOver={(e) => handleDrag(e, fileType)}
        onDrop={(e) => handleDrop(e, setter)}
      >
        <input 
          className="file-input-hidden" 
          type="file" 
          accept="application/pdf" 
          onChange={e => setter(e.target.files[0])}
          id={`file-${fileType}`}
        />
        <label htmlFor={`file-${fileType}`} className="file-drop-label">
          <div className="file-drop-content">
            <div className="file-icon">
              {icon}
            </div>
            <div className="file-text">
              <h3 className="file-title">{label}</h3>
              <p className="file-description">{description}</p>
              {file ? (
                <div className="file-selected">
                  <div className="file-check">✓</div>
                  <span className="file-name">{file.name}</span>
                </div>
              ) : (
                <span className="file-prompt">Click to browse or drag & drop</span>
              )}
            </div>
          </div>
        </label>
      </div>
    </div>
  );

  const DocumentIcon = () => (
    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  );

  const InvoiceIcon = () => (
    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
    </svg>
  );

  const ClipboardIcon = () => (
    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
    </svg>
  );

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="header-left">
            <div className="logo-container">
            <img 
                  src="/netcarelogo.png" 
                  alt="Netcare Logo" 
                  className="w-auto h-12 object-contain"
                />
              <div>
                <h1 className="header-title">NetcarePlus</h1>
                <p className="header-subtitle">GapCare Assessment</p>
              </div>
            </div>
          </div>
          <div className="header-right">
            <div className="user-badge">
              <div className="user-avatar">
                <span>CA</span>
              </div>
              <span className="user-text">Claims Assessor</span>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-badge">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            AI-Powered Assessment
          </div>
          <h2 className="hero-title">GapCover Claim Pre-Assessment</h2>
          <p className="hero-description">
            Upload your documents for instant AI-powered claim assessment with comprehensive rule validation
          </p>
        </div>
      </section>

      {/* Main Content */}
      <main className="main-content">
        <div className="upload-section">
          <div className="section-header">
            <h3 className="section-title">Document Upload</h3>
            <p className="section-description">
              Please upload all three required documents to proceed with the assessment
            </p>
          </div>

          <div className="upload-grid">
            <FileUploadArea
              file={medical}
              setter={setMedical}
              label="Medical Scheme Statement"
              description="Upload your medical scheme statement PDF"
              fileType="medical"
              icon={<DocumentIcon />}
            />
            
            <FileUploadArea
              file={provider}
              setter={setProvider}
              label="Provider Invoice"
              description="Upload the healthcare provider invoice PDF"
              fileType="provider"
              icon={<InvoiceIcon />}
            />
            
            <FileUploadArea
              file={claim}
              setter={setClaim}
              label="Claim Form"
              description="Upload the completed GapCover claim form PDF"
              fileType="claim"
              icon={<ClipboardIcon />}
            />
          </div>

          <div className="upload-actions">
            <div className="upload-status">
              <div className="status-indicator">
                <div className={`status-dot ${allUploaded ? 'status-complete' : 'status-pending'}`}></div>
                <span className="status-text">
                  {allUploaded ? 'All documents uploaded' : `${[medical, provider, claim].filter(Boolean).length}/3 documents uploaded`}
                </span>
              </div>
            </div>
            
            <button 
              className={`assess-button ${loading ? 'loading' : ''}`}
              onClick={handleSubmit} 
              disabled={loading || !allUploaded}
            >
              {loading ? (
                <>
                  <div className="loading-spinner"></div>
                  Processing Assessment...
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                  Run Pre-Assessment
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results Section */}
        {result && result.result && (
          <div className="results-section animate-fade-in">
            <div className="results-header">
              <h3 className="results-title">Assessment Results</h3>
              <div className={`coverage-badge ${result.result?.covered ? 'covered' : 'not-covered'}`}>
                {result.result?.covered ? '✓ Covered' : '✗ Not Covered'}
              </div>
            </div>

            <div className="results-grid">
              {/* Main Result Card */}
              <div className="result-card main-result">
                <div className="result-header">
                  <div className={`result-icon ${result.result?.covered ? 'success' : 'error'}`}>
                    {result.result?.covered ? '✓' : '✗'}
                  </div>
                  <div>
                    <h4 className="result-status">
                      {result.result?.covered ? 'Claim Approved' : 'Claim Declined'}
                    </h4>
                    {result.result?.payable_amount_ZAR && (
                      <p className="result-amount">{result.result?.payable_amount_ZAR}</p>
                    )}
                  </div>
                </div>

                {result.result?.benefits && result.result.benefits.length > 0 && (
                  <div className="benefits-section">
                    <h5 className="benefits-title">Applicable Benefits</h5>
                    <div className="benefits-list">
                      {result.result.benefits.map((benefit, index) => (
                        <div key={index} className="benefit-item">
                          <div className="benefit-dot"></div>
                          <span>{benefit}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Explanation Card */}
              <div className="result-card">
                <h4 className="card-title">Detailed Explanation</h4>
                <p className="explanation-text">{result.result?.explanation}</p>
              </div>

              {/* Actions Card */}
              <div className="result-card">
                <h4 className="card-title">Actions</h4>
                <div className="action-buttons">
                  {result.pdf && (
                    <a 
                      className="action-button primary"
                      href={`data:application/pdf;base64,${result.pdf}`} 
                      download="assessment-report.pdf"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Download Report
                    </a>
                  )}
                  <button 
                    className="action-button secondary"
                    onClick={() => {
                      setResult(null);
                      setMedical(null);
                      setProvider(null);
                      setClaim(null);
                    }}
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    New Assessment
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-content">
          <div className="footer-disclaimer">
            <div className="disclaimer-icon">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </div>
            <div>
              <p className="disclaimer-title">Demo Assessment Only</p>
              <p className="disclaimer-text">
                Human audit required before payment. This assessment is generated by an AI system and should be reviewed by a qualified claims assessor.
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}