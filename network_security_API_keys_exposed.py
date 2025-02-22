import requests
import re

# Define regex patterns for common API keys
api_key_patterns = [
    r"AIza[0-9A-Za-z-_]{35}",          # Google API Key
    r"sk_live_[0-9a-zA-Z]{24}",         # Stripe Live Key
    r"[0-9a-f]{32}-us[0-9]{1,2}",       # Mailchimp API Key
    r"ghp_[0-9a-zA-Z]{36}",             # GitHub Personal Access Token
    r"SG\.[0-9A-Za-z-_]{22}\.[0-9A-Za-z-_]{43}"  # SendGrid API Key
]

def scan_website_for_api_keys(url):
    """
    Fetch the content of the given URL and scan for exposed API keys.
    Returns a dictionary of found keys or an empty dict if none are found.
    """
    try:
        headers = {
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/110.0.0.0 Safari/537.36")
        }
        response = requests.get(url, headers=headers, timeout=5)
        content = response.text
        
        found_keys = {}  # key: regex pattern, value: list of matches
        for pattern in api_key_patterns:
            matches = re.findall(pattern, content)
            if matches:
                found_keys[pattern] = matches
        return found_keys

    except requests.exceptions.RequestException as e:
        print(f"Error scanning {url}: {e}")
        return {}

# Example integration into your website scanner:
if __name__ == "__main__":
    # List of websites to scan
    websites = [
        'https://umanitoba.ca',
        'https://glitchsecure.com',
        'https://hsgs.edu.vn'
    ]
    
    for url in websites:
        print(f"\nScanning {url} for API keys...")
        keys_found = scan_website_for_api_keys(url)
        if keys_found:
            print("Potential API keys found:")
            for pattern, keys in keys_found.items():
                for key in keys:
                    print(f" - {key}")
        else:
            print("No API keys found or an error occurred.")
