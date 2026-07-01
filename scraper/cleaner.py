import json

INPUT_FILE = "shl-ai/data/catalog.json"
OUTPUT_FILE = "shl-ai/data/catalog_clean.json"

REMOVE_PHRASES = [
    "We recommend upgrading to a modern browser.",
    "If you choose to continue with your current browser we cannot guarantee your experience.",
    "Discover how we can transform your talent decisions today.",
    "Strengthen your workforce",
    "Reboot your technology hiring process",
    "Help new and mid-level managers",
    "With our platform of pre-configured",
    "SHL and its affiliates. All rights reserved."
]

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    catalog = json.load(f)

for item in catalog:

    description = item.get("description", "")

    for phrase in REMOVE_PHRASES:
        description = description.replace(phrase, "")

    # Remove extra spaces
    description = " ".join(description.split())

    item["description"] = description

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=4)

print("Clean catalog saved.")