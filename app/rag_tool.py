# Copyright 2026 Google LLC
# RAG Engine retrieval tools for easy-travel agent

import vertexai
from vertexai import rag

PROJECT_ID = "qwiklabs-gcp-03-75c5785951f4"
RAG_LOCATION = "us-central1"
TRAVEL_HANDBOOK_CORPUS = "projects/1089479494300/locations/us-central1/ragCorpora/1005542966019751936"
HERBAL_CORPUS = "projects/1089479494300/locations/us-central1/ragCorpora/3410465167035596800"


def consult_travel_handbook(query: str) -> str:
    """Search the World Travel Handbook corpus for global emergency phone numbers, passport loss steps, power plug types, TSA baggage rules, tipping etiquette, and city transportation insider tips.

    Args:
        query: What to look up (emergency numbers, plug/voltage advice, airport rules, tipping etiquette, or city transport tips).

    Returns:
        Relevant passages extracted directly from the World Travel Handbook.
    """
    try:
        vertexai.init(project=PROJECT_ID, location=RAG_LOCATION)
        resp = rag.retrieval_query(
            text=query,
            rag_resources=[rag.RagResource(rag_corpus=TRAVEL_HANDBOOK_CORPUS)],
            rag_retrieval_config=rag.RagRetrievalConfig(top_k=4),
        )
        contexts = getattr(resp.contexts, "contexts", [])
        passages = [c.text.strip() for c in contexts if getattr(c, "text", "").strip()]
        if not passages:
            return "No relevant passages found in World Travel Handbook."
        return "\n\n---\n\n".join(passages)
    except Exception as e:
        return f"RAG retrieval error: {e}"


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
            rag_resources=[rag.RagResource(rag_corpus=HERBAL_CORPUS)],
            rag_retrieval_config=rag.RagRetrievalConfig(top_k=4),
        )
        contexts = getattr(resp.contexts, "contexts", [])
        passages = [c.text.strip() for c in contexts if getattr(c, "text", "").strip()]
        if not passages:
            return "No relevant passages found in The Complete Herbal."
        return "\n\n---\n\n".join(passages)
    except Exception as e:
        return f"RAG retrieval error: {e}"
