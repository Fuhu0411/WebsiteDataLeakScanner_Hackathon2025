
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import time

# List of known sensitive data patterns to look for in API responses (e.g., access tokens, passwords)
SENSITIVE_PATTERNS = [
    r"(?i)api_key",  # API key
    r"(?i)access_token",  # Access token
    r"(?i)password",  # Passwords
    r"(?i)secret",  # Secret keys
    r"(?i)auth",  # Authentication related
    r"(?i)private_key",  # Private key
    # Add more patterns as necessary
]

# Common API documentation paths that could indicate unintentional exposure
API_DOC_PATHS = [
    "swagger",
    "api/docs",
    "openapi",
    "postman",
    "v1/docs",
    "api/v1/docs",
    "docs"
]

# Function to crawl the site and get all the links
def crawl_site(base_url):
    links = []
    
    try:
        response = requests.get(base_url)
        if response.status_code != 200:
            print(f"Failed to retrieve {base_url}")
            return []
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <a> tags with href attributes
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(base_url, a_tag['href'])
            if link.startswith(('http://', 'https://')):  # Only add valid HTTP links
                links.append(link)
    
    except requests.exceptions.RequestException as e:
        print(f"Error crawling {base_url}: {e}")
    
    return links

# Function to scan an endpoint for sensitive information and potential vulnerabilities
def scan_endpoint(url):
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            print(f"Scanning {url} for sensitive data and vulnerabilities...")

            # Search for known sensitive data patterns in the response text
            for pattern in SENSITIVE_PATTERNS:
                if re.search(pattern, response.text):
                    print(f"Potential sensitive data leak detected at {url}")
                    print(f"Pattern found: {pattern}")
            
            # Check for common API documentation paths in the URL
            for doc_path in API_DOC_PATHS:
                if doc_path.lower() in url.lower():
                    print(f"Potential API documentation leak detected at {url}")
            
            # Check for error messages or backend details in the response text
            check_error_messages(url, response.text)
        
        else:
            print(f"Failed to retrieve {url} - Status Code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error scanning {url}: {e}")

# Function to check for error messages or backend details in the response content
def check_error_messages(url, content):
    # Look for stack traces or backend-related error messages
    error_patterns = [
        r"stack trace",  # Stack trace pattern
        r"database error",  # Database error pattern
        r"mysql",  # MySQL version information in error messages
        r"pgsql",  # PostgreSQL version info in error messages
        r"apache",  # Apache version info in error messages
        r"server error",  # General server error pattern
        r"403 Forbidden",  # Forbidden error indicating misconfiguration
        r"500 Internal Server Error"  # Internal server error
    ]
    
    for pattern in error_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"Potential error message or backend information leak detected at {url}")
            print(f"Pattern found: {pattern}")

# Main function to orchestrate scanning
def main():
    base_url = input("Enter the base URL to scan (e.g., http://example.com): ").strip()
    
    # Crawl the site for links (you can limit the number of pages if needed)
    links = crawl_site(base_url)
    
    # Scan each link found
    for link in links:
        scan_endpoint(link)
        time.sleep(1)  # Delay to avoid hammering the server with requests too fast

# Run the scanner
if __name__ == "__main__":
    main()
