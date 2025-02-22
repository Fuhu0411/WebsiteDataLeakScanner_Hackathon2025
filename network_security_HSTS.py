import requests
import re

def clean_domain(url):
    """Ensure the URL starts with HTTP for testing redirects."""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url  # Start with HTTP to check redirection
    return url.rstrip("/")  # Remove trailing slash

def check_http_redirect(url):
    """Check if a website automatically redirects HTTP to HTTPS."""
    url = clean_domain(url)  # Ensure correct format

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/110.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=False)

        if response.status_code in [301, 302, 307, 308]:  # Redirect status codes
            redirect_location = response.headers.get("Location", "")
            if redirect_location.startswith("https://"):
                print(f"\n✅ {url} redirects to HTTPS: {redirect_location}")
                return redirect_location  # Return the redirected HTTPS URL for HSTS check
            else:
                print(f"\n⚠️ {url} redirects, but NOT to HTTPS! ({redirect_location})")
                return None
        else:
            print(f"\n❌ {url} does NOT redirect to HTTPS!")
            print("   🚨 Users can connect over insecure HTTP, which is a security risk.")
            return None

    except requests.exceptions.ConnectionError:
        print(f"[❌] Connection Error: Could not reach {url}.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[❌] Failed to fetch redirect status for {url}: {e}")
        return None

def check_hsts(url):
    """Check if a website has HSTS enabled (Forces HTTPS)."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/110.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)

        if "Strict-Transport-Security" in response.headers:
            print(f"✅ {url} has HSTS enabled! (Forces HTTPS at browser level)")
            print(f"   🔒 {response.headers['Strict-Transport-Security']}")
        else:
            print(f"⚠️ {url} does NOT enforce HSTS!")
            print("   ❌ This means users may be vulnerable to MITM attacks if they connect over HTTP.")

    except requests.exceptions.SSLError:
        print(f"[❌] SSL Error: {url} may not support HTTPS.")
    except requests.exceptions.ConnectionError:
        print(f"[❌] Connection Error: Could not reach {url}.")
    except requests.exceptions.RequestException as e:
        print(f"[❌] Failed to fetch headers for {url}: {e}")


def checking_hsts(urls):
    # Prompt the user for multiple URLs separated by commas
    
   

    for url in urls:
        url = url.strip()
        print(f"\n=== Testing URL: {url} ===")
        redirected_url = check_http_redirect(url)
        if redirected_url:
            check_hsts(redirected_url)
