import crawler
import network_security_HTTPS
import network_security_Encryption_Protocol
import network_security_SSL
import network_security_HSTS
import network_security_X_FRAME


def main_file():
    """Ask user for a website URL and check if HTTPS is enabled"""
    url = input("Enter the website URL (e.g., http://example.com): ").strip()


    #Crawl
    https_links =crawler.extract_external_links(url)


    if len(https_links)>0:
        print("\n🔗 External HTTPS Links Found:")
        for link in https_links:
            print(link)

    print(f"\n\n--CHECKING TLS CERTIFICATES--\n")
    #Checking https_links for TLS encryption
    network_security_Encryption_Protocol.check_encryption_protocol(https_links)


    print(f"\n\n--CHECKING SSL CERTIFICATES--\n")
    #Checking https_links for SSL certificates
    network_security_SSL.check_encryption_protocol_for_hosts(https_links)


    print(f"\n\n--CHECKING HSTS--\n")
    network_security_HSTS.checking_hsts(https_links)

    print(f"\n\n--CHECKING X-FRAME--\n")
    network_security_X_FRAME.checking_x_frame(https_links)


main_file()