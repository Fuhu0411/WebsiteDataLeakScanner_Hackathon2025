import ssl
import socket
import re

def clean_domain(url):
    """Extracts the domain name from a URL."""
    url = re.sub(r"^https?://", "", url)  # Remove http:// or https://
    url = url.rstrip("/")  # Remove trailing slash if present
    return url

def check_encryption_protocol(domain):
    """Check if a website supports HTTPS or only HTTP."""
    domain = clean_domain(domain)

    try:
        # Try connecting over HTTPS
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                protocol_used = ssock.version()
        print(f"\n🔍 Checking Encryption Protocol for: {domain}")
        print(f"   🔄 Encryption Protocol Used: {protocol_used}")
        print("✅ Secure: The website supports HTTPS.")

    except (socket.timeout, ssl.SSLError, ConnectionResetError):
        print(f"\n⚠️ {domain} **does NOT support HTTPS!**")
        print("❌ This means all communication is in plain text and can be intercepted.")
        print("🔴 Users should avoid entering sensitive data on this site.")

if __name__ == "__main__":
    url = input("Enter website domain (e.g., example.com): ").strip()
    check_encryption_protocol(url)