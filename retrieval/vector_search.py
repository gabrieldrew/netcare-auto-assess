import os
import pickle

import faiss
import numpy as np

from config.openai_config import get_client

INDEX_PATH = os.path.join(
    os.path.dirname(__file__), "..", "embeddings", "policy_index.faiss"
)
META_PATH = os.path.join(
    os.path.dirname(__file__), "..", "embeddings", "policy_chunks.pkl"
)


def load_policy_index():
    if not os.path.exists(INDEX_PATH):
        raise RuntimeError("Policy index not found. Run embeddings/embed_policy.py.")
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        chunks = pickle.load(f)
    return (index, chunks)


def _combined_excerpt(claim_struct: dict) -> str:
    """Return text snippet for embedding search from various claim formats."""

    if "raw_excerpt" in claim_struct:
        return claim_struct["raw_excerpt"][:1000]

    parts = []
    provider = claim_struct.get("provider_statement", {})
    medical_aid = claim_struct.get("medical_aid_statement", {})
    if isinstance(provider, dict) and provider.get("raw_excerpt"):
        parts.append(provider["raw_excerpt"])
    if isinstance(medical_aid, dict) and medical_aid.get("raw_excerpt"):
        parts.append(medical_aid["raw_excerpt"])

    return "\n".join(parts)[:1000]


def retrieve_rules(index_tuple, claim_struct, k: int = 5):
    index, chunks = index_tuple
    client = get_client()
    emb = (
        client.embeddings.create(
            input=[_combined_excerpt(claim_struct)],
            model="text-embedding-3-large",
        )
        .data[0]
        .embedding
    )
    D, I = index.search(np.array([emb], dtype="float32"), k)
    return [chunks[i] for i in I[0]]
