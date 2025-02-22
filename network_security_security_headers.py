import requests

# List of important security headers to check
SECURITY_HEADERS = [
    "Strict-Transport-Security",  # HSTS: Forces HTTPS
    "Content-Security-Policy",    # CSP: Helps prevent XSS attacks
    "X-Frame-Options",            # Protects against clickjacking
    "X-Content-Type-Options",     # Prevents MIME-type sniffing
    "Referrer-Policy",            # Controls how referrer info is shared
    "Permissions-Policy"          # Controls access to browser features
]

def check_security_headers(url):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        
        print(f"\n🔍 Checking security headers for: {url}\n")

        # Loop through the headers we want to check
        for header in SECURITY_HEADERS:
            if header in response.headers:
                print(f"✅ {header}: {response.headers[header]}")
            else:
                print(f"❌ {header} is missing!")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    target_url = input("Enter website URL to check (include http:// or https://): ")
    check_security_headers(target_url)
import requests

# List of important security headers to check
SECURITY_HEADERS = [
    "Strict-Transport-Security",  # HSTS: Forces HTTPS
    "Content-Security-Policy",    # CSP: Helps prevent XSS attacks
    "X-Frame-Options",            # Protects against clickjacking
    "X-Content-Type-Options",     # Prevents MIME-type sniffing
    "Referrer-Policy",            # Controls how referrer info is shared
    "Permissions-Policy"          # Controls access to browser features
]

def check_security_headers(url):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        
        print(f"\n🔍 Checking security headers for: {url}\n")

        # Loop through the headers we want to check
        for header in SECURITY_HEADERS:
            if header in response.headers:
                print(f"✅ {header}: {response.headers[header]}")
            else:
                print(f"❌ {header} is missing!")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    target_url = input("Enter website URL to check (include http:// or https://): ")
    check_security_headers(target_url)
