.PHONY: setup embed run-backend run-frontend

setup:
	sudo apt-get update
	sudo apt-get install -y tesseract-ocr poppler-utils
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

embed:
	venv/bin/python -m embeddings.embed_policy data/static/policy_rules.yml

run-backend:
	venv/bin/uvicorn backend.main:app --reload --port 8000

run-frontend:
	cd frontend && npm install && npm run dev
