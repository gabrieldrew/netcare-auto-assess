"""
Usage:
    python embeddings/embed_policy.py data/static/policy_rules.pdf
Saves FAISS index + chunk list in `embeddings/`.
"""

import argparse
import os
import pickle

import faiss
import numpy as np

from config.openai_config import get_client
from ocr.pdf_reader import extract_text_from_pdf
from utils.text_utils import chunk_text

INDEX_PATH = os.path.join(os.path.dirname(__file__), "policy_index.faiss")
META_PATH = os.path.join(os.path.dirname(__file__), "policy_chunks.pkl")


def build_index(pdf_path: str):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    client = get_client()
    embeddings = client.embeddings.create(
        input=chunks, model="text-embedding-3-large"
    ).data
    mat = np.vstack([e.embedding for e in embeddings]).astype("float32")
    index = faiss.IndexFlatL2(mat.shape[1])
    index.add(mat)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(chunks, f)
    print(f"Embedded {len(chunks)} chunks. Index saved to {INDEX_PATH}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", help="Path to policy PDF")
    args = ap.parse_args()
    build_index(args.pdf)
