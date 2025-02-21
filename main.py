import crawler


def main_file():
    """Ask user for a website URL and check if HTTPS is enabled"""
    url = input("Enter the website URL (e.g., http://example.com): ").strip()

    print(f"Url: {url}")

    #Crawl
    found_links =crawler.crawl_website(url)

main_file()