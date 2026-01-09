from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

class MemoryMoat:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = Chroma(embedding_function=self.embeddings, collection_name="moat_memory")
        self.short_term = {}  # Ephemeral dict for session context

    def add_memory(self, text, metadata=None):
        """Store long-term memory."""
        self.vector_store.add_texts([text], metadatas=[metadata or {}])

    def retrieve(self, query, k=3):
        """RAG-style retrieval."""
        return self.vector_store.similarity_search(query, k=k)

    def add_short_term(self, key, value):
        self.short_term[key] = value

    def get_short_term(self, key):
        return self.short_term.get(key)