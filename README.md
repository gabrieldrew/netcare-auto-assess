# Netcare Auto Assess – Demo Claim Pre‑Assessment

This repo is a **minimal demo** of a pipeline that:
1. Loads the static GapCare policy PDF, chunks & embeds it to a FAISS index.
2. Accepts two PDFs (medical scheme statement + provider invoice).
3. OCRs/extracts text, parses key fields.
4. Retrieves relevant policy rules.
5. Asks GPT‑4o‑mini for a JSON pre‑assessment.

## Quick start
```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt

# One‑time: embed the policy document
python embeddings/embed_policy.py data/static/policy_rules.pdf

# Run the Streamlit app
streamlit run app.py
```

Set `OPENAI_API_KEY` in .env before running.

## Repo layout
See the directory tree for module purpose.  Each sub‑package has a single file
to keep the demo small.