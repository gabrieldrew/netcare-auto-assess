"""
Build a FAISS index from either:
 • a PDF  (extracts text & chunks)
 • a YAML rules file (loads YAML, flattens each rule block)
Run:
    venv/bin/python -m embeddings.embed_policy data/static/policy_rules.yml
"""

import argparse
import json
import os
import pickle

import faiss
import numpy as np
import yaml

from config.openai_config import get_client
from ocr.pdf_reader import extract_text_from_pdf
from utils.text_utils import chunk_text

INDEX_PATH = os.path.join(os.path.dirname(__file__), "policy_index.faiss")
META_PATH = os.path.join(os.path.dirname(__file__), "policy_chunks.pkl")


def load_yaml_as_chunks(path: str) -> list[str]:
    """Return one chunk per rule (id + title + flattened JSON)."""
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    chunks = []
    for rule in data.get("rules", []):
        # pretty-dump each rule so GPT can read it naturally
        header = f"{rule.get('id')} – {rule.get('title')}"
        body = json.dumps(rule, indent=2, ensure_ascii=False)
        chunks.append(f"{header}\n{body}")
    # meta block as one extra chunk
    meta_txt = "POLICY_META\n" + json.dumps(data.get("meta", {}), indent=2)
    chunks.append(meta_txt)
    return chunks


def build_index(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext in {".yml", ".yaml"}:
        chunks = load_yaml_as_chunks(path)
    elif ext == ".pdf":
        text = extract_text_from_pdf(path)
        chunks = chunk_text(text)
    else:
        raise ValueError("Unsupported file type. Use .pdf, .yml, or .yaml")

    client = get_client()
    # Embed in batches to avoid 8192-input hard limit
    embeds = []
    for ch in chunks:
        embeds.append(
            client.embeddings.create(input=[ch], model="text-embedding-3-large")
            .data[0]
            .embedding
        )
    mat = np.vstack(embeds).astype("float32")
    index = faiss.IndexFlatL2(mat.shape[1])
    index.add(mat)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(chunks, f)
    print(f"Indexed {len(chunks)} chunks → {INDEX_PATH}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="Path to rules PDF or YAML")
    args = ap.parse_args()
    build_index(args.path)
