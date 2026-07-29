from dataclasses import dataclass

import chromadb
from sentence_transformers import SentenceTransformer

from rag.config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
)


@dataclass
class RetrievedDocument:
    content: str
    source: str
    distance: float | None


_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    """Load the embedding model once and reuse it."""

    global _model

    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    return _model


def retrieve(
    query: str,
    top_k: int = 2,
) -> list[RetrievedDocument]:
    """Retrieve the most relevant Houdini knowledge documents."""

    query = query.strip()

    if not query:
        raise ValueError("The retrieval query cannot be empty.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    if not CHROMA_DIR.exists():
        raise FileNotFoundError(
            "Chroma database does not exist. "
            "Run `uv run python -m rag.ingest` first."
        )

    model = get_embedding_model()

    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception as error:
        raise RuntimeError(
            f"Collection '{COLLECTION_NAME}' was not found. "
            "Run `uv run python -m rag.ingest` first."
        ) from error

    available_documents = collection.count()

    if available_documents == 0:
        return []

    result_count = min(top_k, available_documents)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=result_count,
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents") or [[]]
    metadatas = results.get("metadatas") or [[]]
    distances = results.get("distances") or [[]]

    retrieved: list[RetrievedDocument] = []

    for index, content in enumerate(documents[0]):
        metadata = metadatas[0][index] or {}
        distance = distances[0][index]

        retrieved.append(
            RetrievedDocument(
                content=content,
                source=str(metadata.get("source", "unknown")),
                distance=float(distance) if distance is not None else None,
            )
        )

    return retrieved


def format_retrieved_context(
    documents: list[RetrievedDocument],
) -> str:
    """Convert retrieved documents into prompt-ready text."""

    if not documents:
        return "No relevant Houdini reference was retrieved."

    sections: list[str] = []

    for index, document in enumerate(documents, start=1):
        sections.append(
            "\n".join(
                [
                    f"## Reference {index}",
                    f"Source: {document.source}",
                    "",
                    document.content,
                ]
            )
        )

    return "\n\n".join(sections)


def main() -> None:
    query = input("Enter a Houdini request: ").strip()

    documents = retrieve(query, top_k=2)

    print("\nRetrieved context:\n")
    print(format_retrieved_context(documents))

    print("\nRetrieval details:")

    for document in documents:
        print(
            f"- source={document.source}, "
            f"distance={document.distance}"
        )


if __name__ == "__main__":
    main()