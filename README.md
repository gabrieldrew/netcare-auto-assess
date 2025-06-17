---

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

    ⚠️ This **will install Tesseract OCR and Poppler globally** on your system.

    ---

    ### 💾 Embed the policy document

    ```bash
    make embed
    ```

    This will process `data/static/policy_rules.pdf` and save the FAISS index in `embeddings/`.

    ---

    ### ▶️ Run the Streamlit app

    ```bash
    make run
    ```

    Launches the demo UI where you can upload medical statements and get automated pre-assessments.

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

    ---