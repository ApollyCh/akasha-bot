from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class FaissDB:
    def __init__(self, model_name, dimension: int = 384):
        self.model = SentenceTransformer(model_name, truncate_dim=dimension)
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add_documents(self, texts: list):
        embeddings = np.array([self.model.encode(text) for text in texts]).astype("float32")

        self.index.add(embeddings)
        self.documents.extend(texts)

        print("Added documents to the FAISS index")

    def search(self, query: str, top_k: int = 5):
        query_embedding = np.array(self.model.encode([query])).astype("float32")

        _, indexes = self.index.search(query_embedding, top_k)

        results = [self.documents[index] for index in indexes[0]]

        return results
