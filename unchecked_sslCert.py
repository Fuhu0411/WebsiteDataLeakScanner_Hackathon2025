import ssl
import socket
from datetime import datetime

def get_certificate(hostname):
    # Create an SSL context
    context = ssl.create_default_context()
    # Connect to the host over SSL
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
    
    conn.connect((hostname, 443))
    cert = conn.getpeercert()

    return cert

def check_validity_period(cert):
    # Define the date format matching the provided string format (e.g., "Feb  3 08:36:05 2025 GMT")
    date_format = "%b %d %H:%M:%S %Y GMT"
    
    # Convert the 'Not Before' and 'Not After' from string to datetime objects
    not_before = datetime.strptime(cert['notBefore'], date_format)
    not_after = datetime.strptime(cert['notAfter'], date_format)
    
    # Get the current time (UTC) to compare with the validity period
    current_time = datetime.utcnow()
    
    # Print certificate validity period
    print("\nValidity Period:")
    print(f"  Not Before: {not_before}")
    print(f"  Not After: {not_after}")
    
    # Check if current time is within the validity period
    if not_before <= current_time <= not_after:
        print("The current time is within the validity period.")
    else:
        print("The current time is outside the validity period.")

# Fetch the certificate for a given hostname
hostname = "www.youtube.com"  # Replace with any domain
cert = get_certificate(hostname)

# Check and print the validity period
check_validity_period(cert)

