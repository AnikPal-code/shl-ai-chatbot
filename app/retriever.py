import json
from pathlib import Path


class AssessmentRetriever:

    def __init__(self):

        base_dir = Path(__file__).resolve().parent.parent
        catalog_path = base_dir / "data" / "catalog_clean.json"

        with open(catalog_path, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

    def search(self, query, k=5):

        query = query.lower()

        scored = []

        for item in self.catalog:

            score = 0

            text = (
                item["name"] + " " +
                item["description"]
            ).lower()

            for word in query.split():

                if word in text:
                    score += 1

            scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [item for _, item in scored[:k]]