import ssl
import socket
import re
import counting_weaknesses
from urllib.parse import urlparse

def clean_domain(url):
    """Extracts the domain name from a full URL."""
    # Remove "http://", "https://", and trailing slashes
    url = re.sub(r"^https?://", "", url)  # Remove http:// or https://
    url = url.rstrip("/")  # Remove trailing slash if present
    return url



def clean_domain(url):
    """Extract and return the domain from a URL."""
    parsed = urlparse(url)
    return parsed.netloc

def check_encryption_protocol(https_links):
    potential_weakness = 0
    """
    Check the encryption protocol (SSL/TLS) used by a list of HTTPS websites.
    https_links should be a set or list of HTTPS URLs.
    """
    for url in https_links:
        # Extract the domain from the URL
        domain = clean_domain(url)

        try:
            # Create an SSL context that supports all TLS versions (but blocks SSLv2 & SSLv3)
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            context.options |= ssl.OP_NO_SSLv2  # Disable SSLv2 (very old, insecure)
            context.options |= ssl.OP_NO_SSLv3  # Disable SSLv3 (very old, insecure)

            # Connect to the website on port 443 (HTTPS)
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    protocol_used = ssock.version()  # Get SSL/TLS version

            # Display results
            print(f"\n🔍 Checking Encryption Protocol for: {domain}")
            print(f"   🔄 Encryption Protocol Used: {protocol_used}")

            # Provide security warnings if needed
            if protocol_used in ["TLSv1.3", "TLSv1.2"]:
                print("✅ Secure: The website is using a modern encryption protocol.")
            elif protocol_used in ["TLSv1.1", "TLSv1.0"]:
                print("⚠️ WARNING: This website is using an outdated encryption protocol!")
                counting_weaknesses.total_possible_weaknesses+=1
            else:
                print("❌ INSECURE: This website might be using an outdated or unknown encryption method.")
                counting_weaknesses.total_possible_weaknesses+=1

        except socket.timeout:
            print(f"[❌] Connection to {domain} timed out.")
            counting_weaknesses.total_possible_weaknesses+=1
        except ssl.SSLError as e:
            print(f"[❌] SSL Error for {domain}: {e}")
            counting_weaknesses.total_possible_weaknesses+=1
        except Exception as e:
            print(f"[❌] Could not check encryption for {domain}: {e}")
            counting_weaknesses.total_possible_weaknesses+=1

    return potential_weakness


