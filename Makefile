.PHONY: setup embed run

setup:
	sudo apt-get update
	sudo apt-get install -y tesseract-ocr poppler-utils
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

embed:
	venv/bin/python -m embeddings.embed_policy data/static/policy_rules.pdf

run:
	venv/bin/streamlit run app.py
