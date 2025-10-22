import os
import uuid
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Default directory for memory persistence
CHROMA_DIR = os.getenv("CHROMA_DB_DIR", "./memory_store")
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"


class MemoryManager:
    def __init__(self, persist_directory: str = CHROMA_DIR):
        """Initialize persistent memory store and embedding model."""
        self.persist_directory = persist_directory
        self.model = SentenceTransformer(EMBED_MODEL_NAME)

        # Use the new PersistentClient API (no Settings / chroma_db_impl)
        self.client = PersistentClient(path=self.persist_directory)

        # Create or load collection
        self.collection = self.client.get_or_create_collection("memory")

    def add_memory(self, text: str, metadata=None):
        emb = self.model.encode([text])[0].tolist()
        self.collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[emb],
            documents=[text],
            metadatas=[metadata or {}],
        )

    def retrieve_similar(self, query: str, k: int = 3):
        """Retrieve memories most similar to a given query."""
        emb = self.model.encode([query])[0].tolist()
        results = self.collection.query(query_embeddings=[emb], n_results=k)

        docs, metas = results.get("documents", [[]])[0], results.get("metadatas", [[]])[0]

        return [
            {"document": d, "metadata": m or {}}
            for d, m in zip(docs, metas)
        ]


    def persist(self):
        """Manually persist the database """
        if hasattr(self.client, "persist"):
            self.client.persist()
