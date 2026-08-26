# Copyright 2026 Google LLC
# RAG Engine retrieval tool for Culpeper's Complete Herbal (pg49513.txt)

import vertexai
from vertexai import rag

PROJECT_ID = "qwiklabs-gcp-03-75c5785951f4"
RAG_LOCATION = "us-central1"
CORPUS_NAME = "projects/1089479494300/locations/us-central1/ragCorpora/3410465167035596800"


def consult_herbal_guide(query: str) -> str:
    """Search Nicholas Culpeper's Complete Herbal book corpus for traditional plant remedies, herbs, and natural health advice.

    Args:
        query: What to look up in the herbal guide (a specific herb, ailment, plant, or remedy).

    Returns:
        Relevant passages extracted directly from Nicholas Culpeper's Complete Herbal.
    """
    try:
        vertexai.init(project=PROJECT_ID, location=RAG_LOCATION)
        resp = rag.retrieval_query(
            text=query,
            rag_resources=[rag.RagResource(rag_corpus=CORPUS_NAME)],
            rag_retrieval_config=rag.RagRetrievalConfig(top_k=4),
        )
        contexts = getattr(resp.contexts, "contexts", [])
        passages = [c.text.strip() for c in contexts if getattr(c, "text", "").strip()]
        if not passages:
            return "No relevant passages found in The Complete Herbal."
        return "\n\n---\n\n".join(passages)
    except Exception as e:
        return f"RAG retrieval error: {e}"
