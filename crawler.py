import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def crawl_website(url, max_pages=50):
    """Crawl a website but limit pages to prevent overloading"""
    visited = set()
    to_visit = [url]

    print(f"🔍 Starting crawl: {url}\n")

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop(0)

        if current_url in visited:
            continue

        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(current_url, headers=headers, timeout=5)

            # Add a delay to avoid being blocked
            time.sleep(1)

            soup = BeautifulSoup(response.text, "html.parser")
            visited.add(current_url)
            print(f"[✅] Found: {current_url}")

            # Extract and add new links
            for link in soup.find_all("a", href=True):
                full_link = urljoin(url, link["href"])
                if full_link.startswith(url) and full_link not in visited:
                    to_visit.append(full_link)

        except requests.exceptions.RequestException:
            print(f"[❌] Failed to crawl: {current_url}")

    print(f"\n✅ Crawling completed. Total Pages Crawled: {len(visited)}")
    # Print discovered links
    print("\n🔗 Discovered URLs:")
    for link in visited:
        print(link)
    return visited


