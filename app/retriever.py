import json
from pathlib import Path


class AssessmentRetriever:

    def __init__(self):

        base_dir = Path(__file__).resolve().parent.parent
        catalog_path = base_dir / "data" / "shl_product_catalog.json"

        with open(catalog_path, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

    def search(self, query, k=5):

        query = query.lower()

        scored = []

        for item in self.catalog:

            text = " ".join([
                item.get("name", ""),
                item.get("description", ""),
                " ".join(item.get("job_levels", [])),
                " ".join(item.get("keys", [])),
                item.get("duration", ""),
            ]).lower()

            score = 0

            for word in query.split():
                if word in text:
                    score += 1

            scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [item for score, item in scored[:k]]