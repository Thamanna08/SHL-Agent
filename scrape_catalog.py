import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}


def scrape_shl_catalog():

    print("Fetching SHL catalog...")

    try:
        response = requests.get(
            CATALOG_URL,
            headers=headers,
            timeout=30
        )

        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print("Failed to fetch catalog")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        catalog = []

        cards = soup.find_all("article")

        print(f"Found {len(cards)} possible assessments")

        for card in cards:

            try:
                title_tag = card.find("h3")

                if not title_tag:
                    continue

                title = title_tag.text.strip()

                link_tag = card.find("a", href=True)

                if not link_tag:
                    continue

                url = link_tag["href"]

                if not url.startswith("http"):
                    url = BASE_URL + url

                description = card.get_text(" ", strip=True)

                lower_text = description.lower()

                if "personality" in lower_text:
                    test_type = "Personality"
                elif "cognitive" in lower_text:
                    test_type = "Cognitive"
                elif "technical" in lower_text:
                    test_type = "Technical"
                else:
                    test_type = "Assessment"

                assessment = {
                    "name": title,
                    "url": url,
                    "description": description,
                    "test_type": test_type
                }

                catalog.append(assessment)

                print(f"Saved: {title}")

                time.sleep(0.1)

            except Exception as e:
                print("Card Error:", e)

        # Remove duplicates
        unique_catalog = []
        seen = set()

        for item in catalog:

            if item["url"] not in seen:

                unique_catalog.append(item)
                seen.add(item["url"])

        with open("shl_catalog.json", "w", encoding="utf-8") as f:
            json.dump(unique_catalog, f, indent=2, ensure_ascii=False)

        print("\n================================")
        print(f"Total saved: {len(unique_catalog)}")
        print("Saved to shl_catalog.json")
        print("================================")

    except Exception as e:
        print("Main Error:", e)


if __name__ == "__main__":
    scrape_shl_catalog()