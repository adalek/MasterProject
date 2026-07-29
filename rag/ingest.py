from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from rag.config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    KNOWLEDGE_DIR,
)


def load_markdown_documents(
    knowledge_dir: Path,
) -> tuple[list[str], list[str], list[dict[str, str]]]:
    """Load each Markdown file as one RAG document."""

    markdown_files = sorted(knowledge_dir.rglob("*.md"))

    if not markdown_files:
        raise FileNotFoundError(
            f"No Markdown files found in: {knowledge_dir}"
        )

    ids: list[str] = []
    documents: list[str] = []
    metadatas: list[dict[str, str]] = []

    for file_path in markdown_files:
        text = file_path.read_text(encoding="utf-8").strip()

        if not text:
            print(f"Skipping empty file: {file_path}")
            continue

        relative_path = file_path.relative_to(knowledge_dir)

        ids.append(relative_path.as_posix())
        documents.append(text)
        metadatas.append(
            {
                "filename": file_path.name,
                "source": relative_path.as_posix(),
            }
        )

    if not documents:
        raise ValueError("All Markdown knowledge files are empty.")

    return ids, documents, metadatas


def rebuild_database() -> None:
    """Rebuild the local Chroma collection from Markdown files."""

    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    ids, documents, metadatas = load_markdown_documents(KNOWLEDGE_DIR)

    print(f"Encoding {len(documents)} documents...")

    embeddings = model.encode(
        documents,
        normalize_embeddings=True,
        show_progress_bar=True,
    ).tolist()

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # 第一版使用完整重建，避免旧数据或重复数据残留。
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted old collection: {COLLECTION_NAME}")
    except Exception:
        # Collection 第一次运行时还不存在。
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": "Verified Houdini Python and SOP knowledge",
            "hnsw:space": "cosine",
        },
    )

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print()
    print("RAG database created successfully.")
    print(f"Documents: {collection.count()}")
    print(f"Database: {CHROMA_DIR}")


if __name__ == "__main__":
    rebuild_database()