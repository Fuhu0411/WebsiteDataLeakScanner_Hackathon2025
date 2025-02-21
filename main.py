import crawler
import network_security_HTTPS

def main_file():
    """Ask user for a website URL and check if HTTPS is enabled"""
    url = input("Enter the website URL (e.g., http://example.com): ").strip()

    print(f"Url: {url}")

    #Crawl
    found_links =crawler.extract_external_links(url)

    #network_security_HTTPS.check_https(found_links)

main_file()