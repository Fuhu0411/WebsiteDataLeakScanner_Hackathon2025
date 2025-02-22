import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse

def extract_hostname(url):
    """
    Extract the hostname from a URL.
    If the URL starts with http:// or https://, it returns the hostname.
    Otherwise, it assumes the input is already a hostname.
    """
    parsed = urlparse(url)
    return parsed.hostname if parsed.hostname else url

def get_certificate(hostname):
    """
    Create an SSL connection to the given hostname on port 443 and return the certificate.
    """
    try:
        # Create an SSL context that uses default settings
        context = ssl.create_default_context()
        # Wrap a socket with the SSL context
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
        return cert
    except Exception as e:
        print(f"[❌] Could not get certificate for {hostname}: {e}")
        return None

def check_validity_period(cert):
    """
    Check and print the validity period of a certificate.
    """
    # Define the date format that matches the certificate date strings
    date_format = "%b %d %H:%M:%S %Y GMT"
    
    try:
        not_before = datetime.strptime(cert['notBefore'], date_format)
        not_after = datetime.strptime(cert['notAfter'], date_format)
    except Exception as e:
        print(f"[❌] Error parsing certificate dates: {e}")
        return

    current_time = datetime.utcnow()

    print("\nValidity Period:")
    print(f"  Not Before: {not_before}")
    print(f"  Not After:  {not_after}")

    if not_before <= current_time <= not_after:
        print("✅ The current time is within the validity period.")
    else:
        print("⚠️ The current time is outside the validity period.")

def check_encryption_protocol_for_hosts(urls):
    """
    Loop through a list of URLs, extract the hostname, get the certificate,
    and check the encryption protocol and validity period.
    """
    for url in urls:
        hostname = extract_hostname(url)
        print(f"\n🔍 Checking {url} (Hostname: {hostname})")
        cert = get_certificate(hostname)
        if cert:
            # Display the SSL/TLS version in use
            try:
                context = ssl.create_default_context()
                context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
                with socket.create_connection((hostname, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        protocol_used = ssock.version()
                print(f"   🔄 Encryption Protocol Used: {protocol_used}")
            except Exception as e:
                print(f"[❌] Could not determine protocol for {hostname}: {e}")
            
            check_validity_period(cert)
        else:
            print(f"[❌] Skipping {hostname} due to certificate retrieval failure.")

