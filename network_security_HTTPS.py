def check_https():
    """Ask user for a website URL and check if HTTPS is enabled"""
    url = input("Enter the website URL (e.g., http://example.com): ").strip()

    if url.startswith("http://"):
        print(f"[⚠️] Warning: {url} is using HTTP, which is insecure!")
    elif url.startswith("https://"):
        print(f"[✅] Good news: {url} is using HTTPS, which is secure.")
    else:
        print(f"[❌] Invalid URL format: {url}")

# Run the function
check_https()
