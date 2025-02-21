import ssl
import socket
import re

def clean_domain(url):
    """Extracts the domain name from a full URL."""
    # Remove "http://", "https://", and trailing slashes
    url = re.sub(r"^https?://", "", url)  # Remove http:// or https://
    url = url.rstrip("/")  # Remove trailing slash if present
    return url

def check_encryption_protocol(domain):
    """Check the encryption protocol (SSL/TLS) used by a website."""
    domain = clean_domain(domain)  # Clean the input

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
        else:
            print("❌ INSECURE: This website might be using an outdated or unknown encryption method.")

    except socket.timeout:
        print(f"[❌] Connection to {domain} timed out.")
    except ssl.SSLError as e:
        print(f"[❌] SSL Error for {domain}: {e}")
    except Exception as e:
        print(f"[❌] Could not check encryption for {domain}: {e}")

if __name__ == "__main__":
    url = input("Enter website URL (e.g., https://example.com/): ").strip()
    check_encryption_protocol(url)