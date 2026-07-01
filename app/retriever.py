import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

class AssessmentRetriever:

    def __init__(self, catalog_path="data/catalog_clean.json"):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        with open(catalog_path, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

        documents = []

        for item in self.catalog:

            text = (
                item["name"]
                + "\n"
                + item["description"]
            )

            documents.append(text)

        embeddings = self.model.encode(
            documents,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

    def search(self, query, k=5):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        scores, indices = self.index.search(query_embedding, k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            
            item = self.catalog[idx].copy()
            item["score"] = float(score)
            
            results.append(item)
            
        return results