import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def extract_external_links(start_url):
    """Access the starting page once and extract external links classified by scheme,
    and also include the start URL in the list."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(start_url, headers=headers, timeout=5)
        html = response.text
    except requests.exceptions.RequestException as e:
        print(f"[❌] Failed to access {start_url}: {e}")
        return set(), set()

    soup = BeautifulSoup(html, "html.parser")
    https_links = set()
    http_links = set()

    # Get the domain of the starting URL
    start_domain = urlparse(start_url).netloc

    # Check the start URL itself and add it to the appropriate set
    parsed_start = urlparse(start_url)
    if parsed_start.scheme.lower() == "https":
        https_links.add(start_url)
    elif parsed_start.scheme.lower() == "http":
        http_links.add(start_url)

    # Extract all <a> tags with href attributes from the starting page
    for link in soup.find_all("a", href=True):
        full_link = urljoin(start_url, link["href"])
        parsed_link = urlparse(full_link)
        scheme = parsed_link.scheme.lower()
        link_domain = parsed_link.netloc

        # Only consider external links (different domain)
        if link_domain and link_domain != start_domain:
            if scheme == "https":
                https_links.add(full_link)
            elif scheme == "http":
                http_links.add(full_link)
            # Optionally, ignore other schemes like mailto or javascript

    #if len(https_links)>0:
     #   print("\n🔗 External HTTPS Links Found:")
      #  for link in https_links:
       #     print(link)

    if len(http_links)>0:
        print("\n⚠️ External HTTP Links Found:")
        for link in http_links:
            print(link)

    return https_links


