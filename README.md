# NetcarePlus GapCare Assessment System

An AI-powered claims assessment system for GapCover insurance policies that automatically processes medical documents and generates claim assessments with detailed PDF reports.

## 🏗️ Tech Stack

### Backend (Python)
- **Framework**: FastAPI - High-performance web framework for building APIs
- **AI/ML**: 
  - OpenAI GPT-4o-mini - For document parsing and claim assessment
  - OpenAI text-embedding-3-large - For semantic search and rule retrieval
- **Document Processing**:
  - PyMuPDF (fitz) - PDF text extraction
  - Pytesseract - OCR for scanned documents  
  - Pillow (PIL) - Image processing
- **Vector Database**: FAISS - Facebook AI Similarity Search for policy rule embeddings
- **Text Processing**: LangChain - Text splitting and chunking utilities
- **PDF Generation**: ReportLab - Professional PDF report creation
- **Configuration**: 
  - PyYAML - Policy rules configuration
  - python-dotenv - Environment variable management
- **Server**: Uvicorn - ASGI server with auto-reload for development

### Frontend (JavaScript/React)
- **Framework**: Next.js 13.5.6 - React framework with server-side rendering
- **Styling**: Tailwind CSS - Utility-first CSS framework with custom Netcare branding
- **UI Components**: Custom React components with Netcare design system
- **Build Tools**: 
  - PostCSS - CSS processing
  - Autoprefixer - Cross-browser CSS compatibility

### Data & Storage
- **Policy Rules**: YAML configuration files for flexible rule management
- **Vector Index**: FAISS binary index files for fast similarity search
- **File Handling**: Multipart form data for PDF uploads
- **Caching**: Pickle serialization for policy chunks metadata

### System Dependencies
- **OCR Engine**: Tesseract OCR - Open source optical character recognition
- **PDF Utils**: Poppler - PDF rendering library for document processing
- **Python Runtime**: Python 3.x with virtual environment isolation

### Development & Deployment
- **Package Management**: 
  - pip (Python dependencies)
  - npm (Node.js dependencies)
- **Build System**: Custom Makefile for streamlined setup and execution
- **Version Control**: Git with comprehensive .gitignore
- **Environment**: Virtual environment (venv) for Python dependency isolation

### AI Model Integration
- **Primary Model**: GPT-4o-mini
  - JSON-structured responses for reliable data extraction
  - Temperature 0.0 for consistent, deterministic outputs
  - Custom prompts for medical document understanding
- **Embedding Model**: text-embedding-3-large
  - High-dimensional vector representations for semantic search
  - Policy rule retrieval based on claim content similarity

### Key Features
- **Intelligent Document Processing**: OCR fallback for scanned PDFs
- **Semantic Rule Matching**: Vector similarity search for relevant policy rules
- **Structured Data Extraction**: AI-powered parsing of claim forms and statements
- **Professional Reporting**: Branded PDF generation with detailed assessments
- **Multi-format Support**: PDF, YAML configuration, and JSON data interchange

## 🛠 Makefile Usage

You can use the provided `Makefile` to set up and run the demo easily.

### 📦 Setup (installs everything you need)

```bash
make setup
```

This will:

- Install required system-level packages (like `tesseract-ocr`) using `apt`
- Create a local Python virtual environment (`venv/`)
- Install all required Python packages inside the `venv`
- Ensure you have Node.js 18+ installed for the Next.js frontend

⚠️ This **will install Tesseract OCR and Poppler globally** on your system.

---

### 💾 Embed the policy document

```bash
make embed
```

This will process `data/static/policy_rules.pdf` and save the FAISS index in `embeddings/`.

---

### ▶️ Run the backend API

```bash
make run-backend
```

Starts a FastAPI server on `http://localhost:8000` that exposes a single `/assess` endpoint.

### ▶️ Run the Next.js frontend

```bash
make run-frontend
```

Launches the React based UI where you can upload PDF documents and view the assessment results.

### Upload PDFs

The app requires three PDFs:

1. Medical Scheme Statement
2. Provider Invoice
3. GapCover Claim Form (AI parsing adds a small OpenAI cost of ~R0.15 per claim)

---

## 🧹 Uninstall / Cleanup

To remove the system packages installed during setup:

```bash
sudo apt-get remove --purge tesseract-ocr poppler-utils
sudo apt-get autoremove
```

Note: This does **not** touch your Python virtual environment or project files.

If you want to clean everything:

```bash
rm -rf venv/ embeddings/policy_index.faiss embeddings/policy_chunks.pkl
```
