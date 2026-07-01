import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

BASE = "https://www.shl.com"

START = "https://www.shl.com/products/assessments/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

visited = set()
queue = deque([START])

assessment_pages = []

while queue:

    url = queue.popleft()

    if url in visited:
        continue

    visited.add(url)

    print("Visiting:", url)

    try:
        response = requests.get(url, headers=HEADERS, timeout=20)

        if response.status_code != 200:
            continue

    except Exception:
        continue

    soup = BeautifulSoup(response.text, "lxml")

    # Collect all assessment links
    for a in soup.find_all("a", href=True):

        href = urljoin(BASE, a["href"])

        if not href.startswith(BASE + "/products/assessments/"):
            continue

        href = href.split("#")[0]
        href = href.split("?")[0]

        if href not in visited:
            queue.append(href)

    # Detect actual assessment pages
    path = url.replace(BASE, "")

    # Assessment pages are deeper than category pages
    if path.count("/") >= 5:

        title = soup.find("h1")

        if title:

            paragraphs = []

            for p in soup.find_all("p"):

                text = p.get_text(" ", strip=True)

                if len(text) > 40:
                    paragraphs.append(text)

            assessment_pages.append(
                {
                    "name": title.get_text(strip=True),
                    "url": url,
                    "description": " ".join(paragraphs)
                }
            )

print("\nFound", len(assessment_pages), "assessment pages")

with open("shl-ai/data/catalog.json", "w", encoding="utf-8") as f:
    json.dump(assessment_pages, f, indent=4)

print("Saved catalog.json")