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
