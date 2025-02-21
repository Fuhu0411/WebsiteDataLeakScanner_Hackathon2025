import crawler
import network_security_HTTPS
import network_security_Encryption_Protocol

def main_file():
    """Ask user for a website URL and check if HTTPS is enabled"""
    url = input("Enter the website URL (e.g., http://example.com): ").strip()


    #Crawl
    https_links =crawler.extract_external_links(url)



    #Checking https_links for TLS encryption
    network_security_Encryption_Protocol.check_encryption_protocol(https_links)

    #network_security_HTTPS.check_https(found_links)

main_file()