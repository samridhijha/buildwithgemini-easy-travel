# Copyright 2026 Google LLC
# Create Vertex AI RAG corpus and import pg49513.txt (The Complete Herbal)

import vertexai
from vertexai import rag

PROJECT_ID = "qwiklabs-gcp-03-75c5785951f4"
LOCATION = "us-central1"
GCS_PATH = "gs://qwiklabs-gcp-03-75c5785951f4-rag/rag/pg49513.txt"
EXISTING_CORPUS_NAME = "projects/1089479494300/locations/us-central1/ragCorpora/3410465167035596800"


def create_and_index_rag():
    print(f"Initializing Vertex AI RAG in project {PROJECT_ID}, location {LOCATION}...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    corpus_name = EXISTING_CORPUS_NAME
    print(f"✓ Using Vertex AI RAG Corpus: {corpus_name}")
    print(f"Indexing {GCS_PATH} into corpus...")
    
    resp = rag.import_files(
        corpus_name=corpus_name,
        paths=[GCS_PATH],
        transformation_config=rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(chunk_size=512, chunk_overlap=100)
        ),
    )
    print(f"✓ Import result: imported {resp.imported_rag_files_count} file(s)")
    print(f"CORPUS_NAME={corpus_name}")
    return corpus_name


if __name__ == "__main__":
    create_and_index_rag()
